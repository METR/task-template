import os
import subprocess

VM_ENVIRONMENT_VARIABLES = [
    "VM_IP_ADDRESS",
    "VM_SSH_USERNAME",
    "VM_SSH_PRIVATE_KEY",
]

ADMIN_KEY_PATH = "/root/.ssh/aws.pem"


def install():
    """Installs necessary libraries on the Docker container for communicating with the aux VM

    Call this function from TaskFamily.install().
    """
    subprocess.check_call("pip install paramiko", shell=True)


def ssh_client():
    """Creates a paramiko SSH client for the admin user of the aux VM

    See https://docs.paramiko.org/en/latest/api/client.html for how to use the client.
    """

    # Make sure we have the SSH key saved to a file
    if not os.path.exists(ADMIN_KEY_PATH):
        with open(ADMIN_KEY_PATH, "w") as f:
            f.write(os.environ["VM_SSH_PRIVATE_KEY"])
        os.chmod(ADMIN_KEY_PATH, 0o600)

        ssh_command = f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i {ADMIN_KEY_PATH} {os.environ['VM_SSH_USERNAME']}@{os.environ['VM_IP_ADDRESS']}"
        print(f"Admin SSH command for aux VM: {ssh_command}")

    import paramiko
    from .aux_ssh_client import SSHClient

    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(ADMIN_KEY_PATH)
    client.connect(
        hostname=os.environ["VM_IP_ADDRESS"],
        username=os.environ["VM_SSH_USERNAME"],
        pkey=private_key,
        banner_timeout=60,  # to resolve timeout issues on connect
    )

    # https://github.com/paramiko/paramiko/issues/918#issuecomment-285882160
    # Need to ping server every once in a while as otherwise server may
    # close connection during long running tasks; if that happens, paramiko
    # will wait forever to hear back from the server (and therefore block
    # forever too!)
    client.get_transport().set_keepalive(interval=60)

    return client


def create_agent_user_step():
    """Returns an aux VM build step for creating an agent user

    Usually this comes first and later steps can set up files in /home/agent.
    """

    return dict(
        type="shell",
        commands=["sudo useradd -m agent"],
    )


def create_agent_user(client):
    """Creates a new user for the agent

    This function is run as part of `setup_agent_ssh()`, so you usually don't need to call it directly.
    """

    stdin, stdout, stderr = client.exec_command("id -u agent")
    if stdout.channel.recv_exit_status() == 0:
        print("User 'agent' already exists on remote VM.")
    else:
        stdin, stdout, stderr = client.exec_command("sudo useradd -m agent")
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("Created user 'agent' on remote VM.")
        else:
            print("Failed to create user 'agent' on remote VM.")

        stdin, stdout, stderr = client.exec_command("sudo usermod -aG root $(whoami)")
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("Granted root privileges to admin account.")
        else:
            print("Failed to grant root privileges to admin account.")

    # Agent shouldn't be able to access the admin directory
    admin_user = os.getenv("VM_SSH_USERNAME")
    client.exec_command(f"sudo chmod 700 /home/{admin_user}")


def setup_agent_ssh(admin=False):
    """Gives the agent an SSH command to access the aux VM

    Call this function in TaskFamily.start().
    """

    if admin:
        # Give the agent root access to the aux VM
        os.makedirs("/home/agent/.ssh", exist_ok=True)
        with open("/home/agent/.ssh/root.pem", "w") as f:
            f.write(os.getenv("VM_SSH_PRIVATE_KEY"))
        os.chmod("/home/agent/.ssh/root.pem", 0o600)
        os.system("sudo chown -R agent:agent /home/agent/.ssh")

        ssh_command = f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /home/agent/.ssh/root.pem {os.environ['VM_SSH_USERNAME']}@{os.environ['VM_IP_ADDRESS']}"

    else:
        with ssh_client() as client:
            # Create a separate user and SSH key for the agent to use
            create_agent_user(client)

            stdin, stdout, stderr = client.exec_command(
                "sudo test -f /home/agent/.ssh/authorized_keys"
            )
            if stdout.channel.recv_exit_status() == 0:
                print("Agent SSH key already uploaded.")
            else:
                # Setup agent SSH directory so we can upload to it
                client.exec_command(f"sudo mkdir -p /home/agent/.ssh")
                client.exec_command(f"sudo chmod 777 /home/agent/.ssh")

                # Create an SSH key for the agent in the Docker container
                os.system(
                    "sudo -u agent ssh-keygen -t rsa -b 4096 -f /home/agent/.ssh/agent.pem -N ''"
                )

                # Upload that key from the Docker container to the aux VM
                sftp = client.open_sftp()
                sftp.put("/home/agent/.ssh/agent.pem.pub", "/home/agent/.ssh/authorized_keys")
                sftp.close()

                # Set correct permissions for SSH files on aux VM
                client.exec_command("sudo chown -R agent:agent /home/agent/.ssh")
                client.exec_command("sudo chmod 700 /home/agent/.ssh")
                client.exec_command("sudo chmod 600 /home/agent/.ssh/authorized_keys")

        ssh_command = f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /home/agent/.ssh/agent.pem agent@{os.environ['VM_IP_ADDRESS']}"

    # Tell the agent how to access the VM
    print(f"Agent SSH command for aux VM: {ssh_command}")
    with open("/home/agent/ssh_command", "w") as f:
        f.write(ssh_command + "\n")
