# METR Task Template

This is a template you can use to develop tasks for the [METR Task Standard](https://github.com/METR/task-standard/).

**Note: If you store your task code on GitHub, please set the repository to "private" so it does not end up in training data for future AI models.**

## Development process
1. Implement your task in [`my_task/my_task.py`](my_task/my_task.py) (rename it with the name of your task)
2. Write tests in [`my_task/tests/test_my_task.py`](my_task/tests/test_my_task.py) (rename it with the name of your task)
3. Use [viv-task-dev](https://github.com/METR/viv-task-dev) to run your task and tests
4. Have someone do a [QA run](https://taskdev.metr.org/quality-assurance/#instructions-for-qa-tester) and document it in [`my_task/meta/qa`](my_task/meta/qa/)
5. Document your task in [`my_task/meta/summary.md`](my_task/meta/summary.md) and [`my_task/meta/detail.md`](my_task/meta/detail.md)
6. Add a [manifest](https://gist.github.com/idavidrein/75e45a6406447e374f2d3403f25bb0b6) in [`my_task/manifest.yaml`](my_task/manifest.yaml)

## Resources

* [Task Development Guide](https://taskdev.metr.org/)
* [METR Task Standard](https://github.com/METR/task-standard/)
* [METR AI R&D tasks](https://github.com/METR/ai-rd-tasks) (good examples of how to build tasks)

## Contact us

If you run into technical issues or have questions about task development, you can email us at [task-support@metr.org](mailto:task-support@metr.org)
