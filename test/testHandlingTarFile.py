from pathlib import Path
from tarfile import TarFile
import unittest


class MyTestCase(unittest.TestCase):

    def test_something(self):
        tarfile = TarFile("ressources/20200414-090526_archive.tar")
        tarfile.extractall(path="ressources")
        tarfile.close()

        sql = Path()
        sql.joinpath("ressources")

        for i in sql.rglob("logicaldoc.sql"):
            self.assertTrue((str(i)).__contains__("ressources/home/cibo/src/backup"))

        for i in sql.rglob("repository/index/"):
            self.assertTrue((str(i)).__contains__("community/repository/index"))

        for i in sql.rglob("repository/docs/"):
            self.assertTrue((str(i)).__contains__("community/repository/docs"))

        for i in sql.rglob("conf/context.properties"):
            self.assertTrue((str(i)).__contains__("conf/context"))
            ret = Path(i)
            self.assertTrue((str(ret.parent)).endswith("conf"))


if __name__ == '__main__':
    unittest.main()
