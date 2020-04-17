import xml.etree.ElementTree as ET
from pathlib import Path

from src.lib.base_reader import BasicReader
from src.lib.variables import XmlKeys as XK


class ReadXML(BasicReader):
    """Class reads and adjusts the conf/log.xml
    """

    def __init__(self, file: Path, value: Path):
        """Constructor.
        :param file: file to alter
        :param value: new logicaldoc-home value
        """
        super().__init__(file, value)
        self.xml_tree = None

    def __alter_log_xml(self):
        """Methode changes old path values to the new logicaldoc-home.
        :return: None
        """
        self.log.info("log.xml is being altered")
        self.xml_tree = ET.parse(self.f)
        root = self.xml_tree.getroot()

        for line in XK.name_value_list:
            ele = root.find("./appender[@name='%s']/param[@name='%s']" % (line[0], XK.PARAM___FILE))
            ele.set(XK.PARAM_KEY_VALUE, self.new_logidoc_path + line[1])

        ET.register_namespace('log4j', 'http://jakarta.apache.org/log4j/')
        self.xml_tree.write(self.f, encoding='utf-8', xml_declaration=True, method='xml')

        doc = open(self.f, encoding='utf-8')
        xml_lines = doc.readlines()
        doc.close()
        with open(self.f, 'w', encoding='utf-8') as doc:
            xml_lines.insert(1, '<!DOCTYPE log4j:configuration SYSTEM "log4j.dtd">\n')  # this way bc ET doesnt support to add doctyp, only package lxml
            doc.writelines(xml_lines)

    def run(self):
        self.__alter_log_xml()
