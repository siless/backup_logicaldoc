import configparser
import unittest
from pathlib import Path

from src.lib.logger import LogicalDocLogger


def _log_stuff(cp):
    with open(str(Path.cwd().joinpath("src/conf/backup.ini")), 'w') as f:
        cp.write(f)
    open(str(Path.cwd().joinpath('src/logs/test.log')), 'w').close()
    log = LogicalDocLogger("test.log").get_prepared_logger()
    log.info("log an info")
    log.warning("log an warning")
    log.debug("log an debug")


class MyTestCase(unittest.TestCase):

    def test_level_debug(self):
        cp = configparser.ConfigParser()
        cp.read(str(Path.cwd().joinpath("src/conf/backup.ini")))
        cp.set('logging', 'level', '10')

        _log_stuff(cp)

        with open(str(Path.cwd().joinpath('src/logs/test.log'))) as f:
            ls = f.readlines()
            self.assertTrue(ls[0].__contains__("- root - INFO - log an info"))
            self.assertTrue(ls[1].__contains__("- root - WARNING - log an warning"))
            self.assertTrue(ls[2].__contains__("- root - DEBUG - log an debug"))

    # @skip("bla")/
    def test_level_warning(self):
        cp = configparser.ConfigParser()
        cp.read(str(Path.cwd().joinpath("src/conf/backup.ini")))
        cp.set('logging', 'level', '30')
        _log_stuff(cp)

        with open(str(Path.cwd().joinpath('src/logs/test.log'))) as f:
            ls = f.readlines()
            self.assertTrue(len(ls), 1)
            self.assertTrue(ls[0].__contains__("- root - WARNING - log an warning"))


if __name__ == '__main__':
    unittest.main()
