r""" watch a directory and reload preset plugins.

"""
# pylint: disable=invalid-name

import sys
import asyncio
from pathlib import Path
from time import sleep
import concurrent

from nonebot import plugin

# from watchgod import awatch
# from watchgod import PythonWatcher as awatch
from watchgod import watch

import logzero
from logzero import logger
logzero.loglevel(10)

CURDIR = Path().absolute().__str__()
COUNT = 0


def _watch_n_reload(watch_dir: str = ""):
    """ watch and reload plugins in a directory.

    Default to the current directory
    """

    _watch_n_reload.flag = False  # break flag

    if not watch_dir:
        watch_dir = CURDIR
    logger.debug("starting watchgod in %s", watch_dir)

    if not Path(watch_dir).is_dir():
        logger.error(" %s is not a directory or does not exist, exiting...")
        return None

    _ = Path(watch_dir).absolute()

    # cache watch_dir absolute path
    _watch_n_reload.watch_dir = _.__str__()

    p_dir = _.parent.__str__()  # parent dir of watch_dir
    # m_dir for module_path needed in the following
    m_dir = _.stem  # module dir name

    # make sure it's a package (__init__.py present)
    if not (_ / "__init__.py").exists():
        logger.error(" __init__.py not present in %s", _)
        logger.info("You need to place an __init__.py in the directory. Exiting... not watching the directory...")
        return None

    # append p_dir to sys.path if not already in sys.path
    if p_dir not in sys.path:
        sys.path.append(p_dir)

    # async for changes in awatch(watch_dir):
    for changes in watch(watch_dir):
        # indicator
        _watch_n_reload.watching = True

        if _watch_n_reload.flag:
            logger.debug("breaking from the changes loop")
            break

        # print("type: ", type(changes), "dir: ", dir(changes))
        # print("changes %s" % changes)
        logger.debug("changes %s", changes)

        list_ = []
        for _ in changes:
            # for _i in _:

            flag, _i = _  # flag: Change.modified, Change.deleted, Change.added
            flag = str(flag)

            logger.debug(" flag: %s, file: %s", flag, _i)

            if flag.endswith("deleted"):
                try:
                    # module_path = f"{Path(CURDIR).stem}.{Path(_i).stem}"
                    # module_path = f"{Path(watch_dir)}.{Path(_i).stem}"
                    module_path = f"{m_dir}.{Path(_i).stem}"
                    res = plugin.PluginManager.remove_plugin(module_path)
                    logger.info("\n\t %s removed: %s", module_path, res)
                except Exception as exc:
                    logger.error("PluginManager.remove exc: %s", exc)
                continue

            _ = """
            if flag.endswith("added"):
                try:
                    module_path = f"{Path(CURDIR).stem}.{Path(_i).stem}"
                    res = plugin.load_plugin(module_path)
                    logger.info(" %s added, %s", module_path, res)
                except Exception as exc:
                    logger.error("plugin.load_plugin exc: %s", exc)
                continue
            # """

            try:
                file_ = Path(_i)
                # if file_.exists():
                list_.append(file_.stem)
            except Exception as exc:
                logger.debug("file_ = Path(_i) exc: %s (expected)", exc)

        logger.info("changed file: *%s*", list_)

        for _ in list_:
            try:
                # _ = str(Path(CURDIR) / _)
                logger.debug(" #reloading %s", _)

                # _ = plugin.reload_plugin(f"plugins1.{_}")

                # module_path = f"{Path(CURDIR).stem}.{_}"
                # module_path = f"{Path(watch_dir)}.{_}"
                module_path = f"{m_dir}.{_}"
                logger.debug(" module_path: %s", module_path)
                res = plugin.reload_plugin(module_path)

                logger.info(" # %s reloaded: [%s]", module_path, res)
            except Exception as exc:
                logger.error(" #plugin.reaload exc: %s", exc)

        # await asyncio.sleep(5)
        sleep(2)

    logger.debug("end of watchgod -- this will only materialize when _watch_n_reload.flag is set to True.")

    _watch_n_reload.watching = False

    return None


# def watch_n_reload(watch_dir: str = ""):
def nbplugins_watch(watch_dir: str = ""):
    """ watch and reaload plugins in a directory.

    Default to the current directory
    """

    try:
        # stop a possible previou watch_god
        _watch_n_reload.flag = True
        logger.debug("resetting _watch_n_reload.flag to True")

        # to trigger some change in the directory
        init_py = Path(_watch_n_reload.watch_dir) / "__init__.py"
        if init_py.exists():
            init_py.touch()
    except Exception as exc:
        logger.debug("_watch_n_reload first run exc: %s (expected)", exc)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    loop = asyncio.get_event_loop()
    # attempt to get a loop in case the loop above is 
    # not available, for example in ipython
    if loop.is_closed():
        loop = asyncio.new_event_loop()
    try:
        loop.run_in_executor(executor, lambda: _watch_n_reload(watch_dir))
    except Exception as exc:
        logger.error("loop.run_in_executor exc: %s", exc)
