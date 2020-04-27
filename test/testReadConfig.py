import unittest

from src.lib.config_reader import ReadConfig


class MyTestCase(unittest.TestCase):

    def test_config_reader(self):
        self.cfg = ReadConfig()
        self.cfg.run()

        self.assertEqual(self.cfg.get_database(), "logicaldoc")
        self.assertEqual(self.cfg.get_host(), "localhost")
        self.assertRaises(SystemExit, self.cfg.get_username)
        self.assertRaises(SystemExit, self.cfg.get_password)

        self.assertIn(int(self.cfg.get_logging_level()), [0, 10, 20, 30, 40, 50])


if __name__ == '__main__':
    unittest.main()
