import unittest

from src.lib.config_reader import ReadConfig


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.cfg = ReadConfig()
        self.cfg.run()



if __name__ == '__main__':
    unittest.main()
