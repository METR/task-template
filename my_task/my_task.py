# This file contains the main code for your task.
# You can delete these comments, and any empty optional methods, before submitting.

from metr_task_standard.types import VMSpec
from typing import TypedDict

# If you try to import third-party libraries here, the task will crash because `install` hasn't run yet.
# You can import libraries in `start` and `score`, which run after `install`.


# The Task class contains data specific to each task in the family.
class Task(TypedDict):
    problem: str
    answer: int


class TaskFamily:
    # Which version of the Task Standard this TaskFamily adheres to
    standard_version = "0.2.2"

    # Optional: a list of environment variable names that must be set in TaskFamily#start
    # and TaskFamily#score (where they can be accessed with e.g. `os.environ.get("MY_ENV_VAR")`).
    required_environment_variables = []

    # `install` is called while building a task-family-specific Docker image.
    # See the Dockerfile for more information about how `install` is called.
    # `install` may install packages, clone Git repos, copy assets into `/home/agent`, or make other such changes.
    # The `install` method (which runs at build time) can access the
    # internet, even if the task will not allow internet access at run time.
    @staticmethod
    def install() -> None:
        pass

    # `get_tasks` returns a mapping from task names to arbitrary data that is specific to each task.
    # `get_tasks` is first called after `install` but before `start`.
    # Note that this method should return the same value every time it is called.
    @staticmethod
    def get_tasks() -> dict[str, Task]:
        return {"addition": {"problem": "1234567 + 2345678", "answer": 1234567 + 2345678}}

    # `get_instructions` returns a string containing initial task instructions for the agent.
    @staticmethod
    def get_instructions(t: Task) -> str:
        problem = t["problem"]
        return f"""Solve the following math problem: {problem}"""

    # `get_permissions` is called after `install` but before `start`.
    # It returns either the empty list or a list containing only the string "full_internet".
    # Refer to the Task Standard more information.
    @staticmethod
    def get_permissions(t: Task) -> list[str]:
        return ["full_internet"]

    # Optional: `get_aux_vm_spec` specifies an auxiliary virtual machine that will be set up along with the task.
    # This is useful if you want to let the agent use a GPU.
    # Refer to the Task Standard for more information.
    @staticmethod
    def get_aux_vm_spec(t: Task) -> VMSpec | None:
        return None

    # `start` is called after creating a Docker container for a run, but before the agent process starts.
    # `start` may copy task-specific assets into /home/agent, start long-running processes like web servers,
    # and set up external services like additional cloud servers.
    @staticmethod
    def start(t: Task) -> None:
        pass

    # `score` is called after the agent submits a solution. If the solution is more complex than a short string,
    # `score` can read files, run programs, make network requests, etc.
    # `score` should return a float between 0 and 1, or `None` to indicate that manual scoring is required.
    @staticmethod
    def score(t: Task, submission: str) -> float | None:
        # Make sure to handle errors if the agent submits an invalid solution
        try:
            answer_int = int(submission)
        except ValueError:
            print("Answer must be an integer")
            return 0

        if answer_int == t["answer"]:
            return 1
        else:
            return 0
        
    # Optional: `teardown` cleans up any external resources created during setup.
    @staticmethod
    def teardown(t: Task) -> None:
        pass
