# nonebot-plugins-watch
![Python3.7 package](https://github.com/ffreemt/nonebot-plugins-watch/workflows/Python3.7%20package/badge.svg) [![codecov](https://codecov.io/gh/ffreemt/nonebot-plugins-watch/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/nonebot-plugins-watch)
 [![PyPI version](https://badge.fury.io/py/nbplugins-watch.svg)](https://badge.fury.io/py/nbplugins-watch)



hot plug and remove nonebot plugins

### Installation

```pip install nbplugins-watch```

To validate installation
```
python -c "import nbplugins_watch; print(nbplugins_watch.__version__)"
0.0.6
```

### Usage
Make a directory somewhere and place an empty \_\_init\_\_.py and a plugin file in it.

Monitor the directory in your nonebot runner file, e.g. in  `my_nonebot.py`:
```python

import nonebot
from nbplugins_watch import nbplugins_watch

nonebot.load_builtin_plugins()  # optional
nonebot.load_plugins("mature_plugins", "mature_plugins")  # optional

plugin_dir_path = r"path_to_plugin_dir"  # absolute or relative path

nbplugins_watch(plugin_dir_path)
# turn annoying debug messages off
# nbplugins_watch(plugin_dir_path, debug=False)

nonebot.run()

```
Create a file, say fancy_plugin.py if not already there, in the directory above. Edit and test and/or remove the file fancy_plugin.py to your heart's content.

Note: currently if you copy a new file to the directory, you need to modify the file at least once to effect a certain plugin. Hopefully this can be fixed in a future version.

### Acknowledgments

* Thanks to everyone whose code was used
