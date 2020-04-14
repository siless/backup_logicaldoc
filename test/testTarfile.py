import shutil
from unittest.mock import patch
import unittest
from pathlib import Path

from src.lib.logger import LogicalDocLogger
from src.operations.backup import Backup


class MyTestCase(unittest.TestCase):



    def setUp(self) -> None:
        self.pf_index = Path("/home/cibo/logicaldoc/community/repository/index/index.txt")
        self.pf_doc = Path("/home/cibo/logicaldoc/community/repository/docs/docs.txt")
        self.pf_conf = Path("/home/cibo/logicaldoc/community/conf/conf.txt")
        self.pf_conf.mkdir(parents=True)
        self.pf_doc.mkdir(parents=True)
        self.pf_index.mkdir(parents=True)

        pass
    @patch('src.operations.backup.run_linux_command', return_value="hatschi")
    def test_something(self, mock_run_linux_command):
        log = LogicalDocLogger("backup.log")
        bkp = Backup(log)
        bkp.backup = Path("/home/cibo/logicaldoc/community")
        bkp.run()
        self.assertTrue(Path("/home/cibo/logicaldoc/community/archive.tar").exists())

        value = bkp.run_linux_command("adsf")
        self.assertEqual(value, "hatschi")

    def tearDown(self) -> None:
        shutil.rmtree("/home/cibo/logicaldoc/")
        pass

if __name__ == '__main__':
    unittest.main()
