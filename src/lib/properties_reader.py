from pathlib import Path

from src.lib.base_reader import BasicReader
from src.lib.variables import PropertiesKeys as PK


class ReadProperties(BasicReader):
    """Class reads and adjusts the conf/context.properties and conf/build.properties
    Property files have specific values with paths where logicaldoc is installed and if you restore your backup to a
    different location, you must alter these paths.
    A handy option would be "pyjavaproperties" via pypi but I want to ovoid external packages, therefore I use very old
    mechanisms
    """

    def __init__(self, file: Path, value: Path):
        """Constructor
        :param file: build.properties or context.properties
        :param value: new value of path
        """
        super().__init__(file, value)

    def __alter_build(self):
        """Method alters values in build.properties
        :return: None
        """
        with open(self.f, 'r') as prop:
            tmp = list()
            for line in prop.readlines():
                if line.__contains__(PK.LOGICALDOC_HOME):
                    self.log.debug("altered %s to %s" % (line, self.new_logidoc_path))
                    tmp.append(PK.LOGICALDOC_HOME + self.new_logidoc_path + "\n")
                else:
                    tmp.append(line)
        with open(self.f, 'w') as prop:  # this way bc prop.truncate(0) does not work properly
            prop.writelines(tmp)

    def __alter_context(self):
        """Method alters values in context.properties
        :return: None
        """
        with open(self.f, 'r') as prop:
            tmp = list()
            for line in prop.readlines():
                tmp.append(self.__get_key_value_pair(line))

        with open(self.f, 'w') as prop:
            prop.writelines(tmp)

    def __get_key_value_pair(self, line: str):
        """Method builds the key-value pair
        :param line: line to alter
        :return: new line with new logicaldoc-home path
        """
        if line.__contains__(PK.LDOCHOME):
            return PK.LDOCHOME + self.new_logidoc_path + "\n"
        elif line.__contains__(PK.ACMECAD_COMMAND):
            return PK.ACMECAD_COMMAND + self.new_logidoc_path + PK.suf_acmecad_command + "\n"
        elif line.__contains__(PK.ACMEDAD_RESOURCE):
            return PK.ACMEDAD_RESOURCE + self.new_logidoc_path + PK.suf_acmedad_resource + "\n"
        elif line.__contains__(PK.CONF_DBDIR):
            return PK.CONF_DBDIR + self.new_logidoc_path + PK.suf_conf_dbdir + "\n"
        elif line.__contains__(PK.CONF_EXPORTDIR):
            return PK.CONF_EXPORTDIR + self.new_logidoc_path + PK.suf_conf_exportdir + "\n"
        elif line.__contains__(PK.CONF_IMPORTDIR):
            return PK.CONF_IMPORTDIR + self.new_logidoc_path + PK.suf_conf_importdir + "\n"
        elif line.__contains__(PK.CONF_IMPORTDIR):
            return PK.CONF_IMPORTDIR + self.new_logidoc_path + PK.suf_conf_importdir + "\n"
        elif line.__contains__(PK.CONF_LOGDIR):
            return PK.CONF_LOGDIR + self.new_logidoc_path + PK.suf_conf_logdir + "\n"
        elif line.__contains__(PK.CONF_PLUGINDIR):
            return PK.CONF_PLUGINDIR + self.new_logidoc_path + PK.suf_conf_plugindir + "\n"
        elif line.__contains__(PK.CONF_USERDIR):
            return PK.CONF_USERDIR + self.new_logidoc_path + PK.suf_conf_userdir + "\n"
        elif line.__contains__(PK.INDEX_DIR):
            return PK.INDEX_DIR + self.new_logidoc_path + PK.suf_index_dir + "\n"
        elif line.__contains__(PK.STORE_1_DIR):
            return PK.STORE_1_DIR + self.new_logidoc_path + PK.suf_store_1_dir + "\n"
        else:
            return line

    def run(self):
        self.log.info("start altering %s" % self.f)
        if self.f.endswith("build.properties"):
            self.__alter_build()
        elif self.f.endswith("context.properties"):
            self.__alter_context()

