from pathlib import Path

from src.lib.base_reader import BasicReader
from src.lib.variables import PropertiesKeys as PK


class ReadProperties(BasicReader):
    """
    Class reads and adjusts the conf/context.properties and conf/build.properties.
    Property files have specific values with paths where logicaldoc is installed and if you restore your backup to a
    different location, you must alter these paths.
    A handy option would be "pyjavaproperties" via pypi but I want to ovoid external packages, therefore I use very old
    mechanisms.
    """

    def __init__(self, file: Path, value: Path):
        """
        Constructor.
        :param file: build.properties or context.properties
        :param value: new value of path
        """
        super().__init__(file, value)

    def __alter_build(self):
        """
        Method alters values in build.properties.
        :return: None
        """
        with open(self.f, 'r') as prop:
            tmp = list()
            for line in prop.readlines():
                if line.__contains__(PK.LOGICALDOC_HOME):
                    new_line = PK.LOGICALDOC_HOME + self.new_logidoc_path + "\n"
                    self.log.debug("altered %s to %s" % (line, new_line))
                    tmp.append(new_line)
                else:
                    tmp.append(line)
        with open(self.f, 'w') as prop:  # this way bc prop.truncate(0) does not work properly
            prop.writelines(tmp)

    def __alter_context(self):
        """
        Method alters values in context.properties.
        :return: None
        """
        with open(self.f, 'r') as prop:
            tmp = list()
            for line in prop.readlines():
                tmp.append(self.__get_key_value_pair(line))

        with open(self.f, 'w') as prop:
            prop.writelines(tmp)

    def __get_key_value_pair(self, line: str):
        """
        Method builds the key-value pair.
        :param line: line to alter
        :return: new line with added new logicaldoc-home path
        """
        for slot in PK.name_value_list:
            if line.__contains__(slot[0]): #slot[0] = prefix (key)
                new_line = slot[0] + self.new_logidoc_path + slot[1] #slot[1] = suffix (value)
                self.log.debug("altered %s to %s" % (line, new_line))
                return new_line + "\n"
        return line

    def run(self):
        self.log.info("start altering %s" % self.f)
        if self.f.endswith("build.properties"):
            self.__alter_build()
        elif self.f.endswith("context.properties"):
            self.__alter_context()

