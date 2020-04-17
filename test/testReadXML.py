import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from src.lib.logger import LogicalDocLogger
from src.lib.xml_reader import ReadXML


class MyTestCase(unittest.TestCase):
    def test_something(self):
        log = LogicalDocLogger("test.log")
        parser = ReadXML(Path("ressources/opt/logidoc/community/conf/log.xml"), Path("/opt/logicaldoc/community"))
        parser.set_logger(log)
        parser.run()

        tree = ET.parse("ressources/opt/logidoc/community/conf/log.xml")
        root = tree.getroot()
        ele = root.find("./appender[@name='DMS']/param[@name='File']")
        self.assertEqual(ele.get('value'), "/opt/logicaldoc/community/repository/logs/dms.log")


if __name__ == '__main__':
    unittest.main()
