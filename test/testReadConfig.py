import unittest
import logging
from src.lib.config_reader import ReadConfig
from src.lib.logger import LogicalDocLogger


class MyTestCase(unittest.TestCase):
    def test_something(self):
        logging.basicConfig(filename="test.log")
        self.cfg = ReadConfig(logging)

        with self.assertRaises(FileNotFoundError) as r:
            self.cfg.run()



if __name__ == '__main__':
    unittest.main()
