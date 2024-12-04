from .. import my_task

# This provides the task and task_family fixtures
pytest_plugins = "metr-task-standard"


def test_correct_answer(task_family: my_task.TaskFamily, task_name: str, task: my_task.Task):
    # If your task requires any setup, first check that it's been performed correctly,
    # e.g. assert that necessary files exist and software is installed.

    # Before submitting an answer, you can perform any actions inside the task container,
    # e.g. modify files or SSH into an aux VM and run a program there.

    submission = str(task["answer"])
    score = task_family.score(task, submission)
    assert score == 1


def test_incorrect_answer(task_family: my_task.TaskFamily, task_name: str, task: my_task.Task):
    submission = str(task["answer"] + 1)
    score = task_family.score(task, submission)
    assert score == 0


def test_invalid_answer(task_family: my_task.TaskFamily, task_name: str, task: my_task.Task):
    submission = "foo"
    score = task_family.score(task, submission)
    assert score == 0
