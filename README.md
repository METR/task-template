# METR Task Template

This is a template you can use to develop tasks for the [METR Task Standard](https://github.com/METR/task-standard/).

**Note: If you store your task code on GitHub, please set the repository to "private" so it does not end up in training data for future AI models.**

## Development process
1. Implement your task in [`my_task/my_task.py`](my_task/my_task.py) (rename it with the name of your task)
2. Write tests in [`my_task/my_task_test.py`](my_task/my_task_test.py) (rename it with the name of your task)
3. Use the [workbench](workbench/) to run your task and tests
4. Have someone do a QA run and document it in [`my_task/meta/qa`](my_task/meta/qa/)
5. Finish documenting your task in [`my_task/meta/summary.md`](my_task/meta/summary.md), [`my_task/meta/detail.md`](my_task/meta/detail.md), and [`my_task/meta/eval_info.json`](my_task/meta/eval_info.json)

## Resources

* [Task Development Guide](https://taskdev.metr.org)
* [METR Task Standard](https://github.com/METR/task-standard/)
    * [Example tasks](https://github.com/METR/task-standard/tree/main/examples)
* [METR public tasks](https://github.com/METR/public-tasks/tree/main/tasks)

## Contact us

If you run into technical issues or have questions about task development, you can email us at [task-support@evals.alignment.org](mailto:task-support@evals.alignment.org)
