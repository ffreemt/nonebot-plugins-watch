# nonebot-plugins-watch
![Python3.7 package](https://github.com/ffreemt/nonebot-plugins-watch/workflows/Python3.7%20package/badge.svg) ![Codecov](https://github.com/ffreemt/nonebot-plugins-watch/workflows/Codecov/badge.svg) [![PyPI version](https://badge.fury.io/py/nbplugins-watch.svg)](https://badge.fury.io/py/nbplugins-watch)

hot plug and remove nonebot plugins

### Installation

```pip install nbplugins-watch```

Validate installation
```
python -c "import nbplugins_watch; print(nbplugins_watch.__version__)"
0.0.1
```

### Usage
Make a directory somewhere and place an empty \_\_init\_\_.py in it.

Monitor the directory in your nonebot runner file, e.g. my_nonebot.py:
```python

import nonebot

nonebot.load_builtin_plugins()  # optioinal

plugin_dir_path = r"path_to_plugin_dir"  # absolute or relative path
from nbplugins_watch import nbplugins_watch
nbplugins_watch(plugin_dir_path)

nonebot.run()

```
Create a file, say fancy_plugin.py, in the directory above. Edit and test and/or remove the file fancy_plugin.py to your heart's content.

Note: if a plugin file contains syntax errors (as opposed to logic errors), you'll have to restart nonebot, in other words, nbplugins_watch will cease to work after an uncaught error.

### Acknowledgments

* Thanks to everyone whose code was used
