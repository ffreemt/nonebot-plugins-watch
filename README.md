# nonebot-plugins-watch ![Python package](https://github.com/ffreemt/nonebot-plugins-watch/workflows/Python3.6|3.7%20package/badge.svg) [![codecov](https://codecov.io/gh/ffreemt/nonebot-plugins-watch/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/nonebot-plugins-watch)
hot plug and remove nonebot plugins

### Installation

```pip install nonebot-plugins-watch```

Validate installation
```
python -c "import nbpugins_watch; print(nbpugins_watch.__version__)"
0.0.1
```

### Usage
Make a directory somewhere and place an empty __init__.py in it.

Monitor the directory in your nonebot runner file, e.g. my_nonebot.py:
```python

import nonebot

nonebot.load_builtin_plugins()  # optioinal

plugin_dir_path = r"path_to_plugin_dir"  # absolute or relative path
from nbpugins_watch import nbpugins_watch
nbpugins_watch(plugin_dir_path)

nonebot.run()

```
Create a file, say fancy_plugin.py, in the directory above. Edit and test and/or remove the file fancy_plugin.py to your heart's content.

Note: if a plugin file contains syntax error (as opposed to logic error), you'll have to restart nonebot, in other words, nbpugins_watch will cease to work after an uncaught error.

### Acknowledgments

* Thanks to everyone whose code was used
