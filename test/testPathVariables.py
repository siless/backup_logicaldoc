import unittest

from src.lib.variables import PathVariables


class MyTestCase(unittest.TestCase):

    def test_something(self):
        self.assertEqual(PathVariables.BACKUP_CONF.__str__(),
                         "/home/cibo/PycharmProjects/backup_logicaldoc/test/src/conf/backup.ini")


if __name__ == '__main__':
    unittest.main()
