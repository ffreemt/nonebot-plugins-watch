r""" watch a directory and reload preset plugins.

"""
# pylint: disable=invalid-name

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
    """ watch and reaload plugins in a directory.

    Default to the current directory
    """

    _watch_n_reload.flag = False  # break flag

    if not watch_dir:
        watch_dir = CURDIR
    logger.debug("starting watchgod in %s", watch_dir)

    if not Path(watch_dir).is_dir():
        logger.error(" %s is not a directory or does not exist, exiting...")
        return None

    # async for changes in awatch(watch_dir):
    for changes in watch(watch_dir):
        if _watch_n_reload.flag:
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
                    module_path = f"{Path(CURDIR).stem}.{Path(_i).stem}"
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

                module_path = f"{Path(CURDIR).stem}.{_}"
                logger.debug(" module_path: %s", module_path)
                res = plugin.reload_plugin(module_path)

                logger.info(" # %s reloaded: [%s]", module_path, res)
            except Exception as exc:
                logger.error(" #plugin.reaload exc: %s", exc)

        # await asyncio.sleep(5)
        sleep(2)

    logger.debug("end of watchgod -- this will only materialize when _watch_n_reload.flag is set to True.")

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
    except Exception as exc:
        logger.debug("_watch_n_reload first run exc: %s (expected)", exc)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, lambda: _watch_n_reload(watch_dir))
