import datetime
import unittest
from pathlib import Path

from src.lib.variables import PathVariables


class MyTestCase(unittest.TestCase):

    def test_variables(self):
        self.assertEqual(PathVariables.BACKUP_CONF.__str__(), str(Path.cwd().joinpath("src/conf/backup.ini")))
        self.assertEqual(PathVariables.SRC__DECOMPRESSED, "src/backup/decompressed/")
        self.assertEqual(PathVariables.SRC__TAR,
                         "src/backup/" + datetime.datetime.now().strftime('%Y%m%d-%H%M%S_') + "archive.tar")


if __name__ == '__main__':
    unittest.main()
