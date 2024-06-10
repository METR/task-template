# Common task code

This folder contains code that might be useful in many different tasks. For example, to use convenience functions for letting the agent access an aux VM, you could do this in `my_task/my_task.py`:

```python
from common import aux_vm_access
```

If you write new code as part of your task that might be useful for other tasks, you can add a file to this directory. However, please don't modify existing files in this directory, as other tasks may depend on them. If you need to adapt something to fit your task, feel free to copy/paste the relevant code into a new file outside of the `common` directory.
