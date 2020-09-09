# nonebot-plugins-watch
![Python3.7 package](https://github.com/ffreemt/nonebot-plugins-watch/workflows/Python3.7%20package/badge.svg) [![codecov](https://codecov.io/gh/ffreemt/nonebot-plugins-watch/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/nonebot-plugins-watch)
 [![PyPI version](https://badge.fury.io/py/nbplugins-watch.svg)](https://badge.fury.io/py/nbplugins-watch)

热拔插nonebot插件

([English README.md](https://github.com/ffreemt/nonebot-plugins-watch/blob/master/README.md))


运行`nbplugins-watch`可监视某个目录，目录里文件更新或被移除时`nonebot`就会自动载入对应更新文件的插件或移除对应的插件（无需重启`nonebot`），应用场景为开发或调试新`nonebot`插件。

### 安装

```pip install nbplugins-watch -U```

### Usage
开个目录并置入 \_\_init\_\_.py 以及插件文件。

在`my_nonebot.py`文件里监控此目录, 例如 `my_nonebot.py`:
```python

import nonebot
from nbplugins_watch import nbplugins_watch

nonebot.load_builtin_plugins()  # 可选
nonebot.load_plugins("mature_plugins", "mature_plugins")  # 可用插件目录，可选

plugin_dir_path = r"path_to_plugin_dir"  # 开发插件目录绝对或相对路径

nbplugins_watch(plugin_dir_path)
# 关掉纠错信息
# nbplugins_watch(plugin_dir_path, debug=False)

nonebot.run()

```
在开发插件目录里编辑插件文件（例如`fancy_plugin.py`，也可新开)，存盘后及时生效。 在qq里测试插件……。 开发好后移入可用插件目录。

注意：新开的插件文件需要在开发插件目录里至少修改存盘一次后才能生效。
