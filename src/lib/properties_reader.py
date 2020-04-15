from pathlib import Path
from configparser import ConfigParser

from src.lib.logger import LogicalDocLogger
from src.lib.variables import PropertiesKeys as _PK


class ReadProperties:
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
        self.f = str(file)
        self.new_logidoc_path = str(value)
        self.log = None

    def __alter_build(self):
        """Method alters values in build.properties
        :return: None
        """
        with open(self.f, 'r') as prop:
            tmp = list()
            for line in prop.readlines():
                if line.__contains__(_PK.LOGICALDOC_HOME):
                    self.log.debug("altered %s to %s" % (line, self.new_logidoc_path))
                    tmp.append(_PK.LOGICALDOC_HOME + self.new_logidoc_path + "\n")
                else:
                    tmp.append(line)
        with open(self.f, 'w') as prop: #this way bc prop.truncate(0) does not work properly
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
        if line.__contains__(_PK.LDOCHOME):
            return _PK.LDOCHOME + self.new_logidoc_path + "\n"
        elif line.__contains__(_PK.ACMECAD_COMMAND):
            return _PK.ACMECAD_COMMAND + self.new_logidoc_path + _PK.suf_acmecad_command + "\n"
        elif line.__contains__(_PK.ACMEDAD_RESOURCE):
            return _PK.ACMEDAD_RESOURCE + self.new_logidoc_path + _PK.suf_acmedad_resource + "\n"
        elif line.__contains__(_PK.CONF_DBDIR):
            return _PK.CONF_DBDIR + self.new_logidoc_path + _PK.suf_conf_dbdir + "\n"
        elif line.__contains__(_PK.CONF_EXPORTDIR):
            return _PK.CONF_EXPORTDIR+self.new_logidoc_path+_PK.suf_conf_exportdir+"\n"
        elif line.__contains__(_PK.CONF_IMPORTDIR):
            return _PK.CONF_IMPORTDIR+self.new_logidoc_path+_PK.suf_conf_importdir+"\n"
        elif line.__contains__(_PK.CONF_IMPORTDIR):
            return _PK.CONF_IMPORTDIR+self.new_logidoc_path+_PK.suf_conf_importdir+"\n"
        elif line.__contains__(_PK.CONF_LOGDIR):
            return _PK.CONF_LOGDIR+self.new_logidoc_path+_PK.suf_conf_logdir+"\n"
        elif line.__contains__(_PK.CONF_PLUGINDIR):
            return _PK.CONF_PLUGINDIR+self.new_logidoc_path+_PK.suf_conf_plugindir+"\n"
        elif line.__contains__(_PK.CONF_USERDIR):
            return _PK.CONF_USERDIR+self.new_logidoc_path+_PK.suf_conf_userdir+"\n"
        elif line.__contains__(_PK.INDEX_DIR):
            return _PK.INDEX_DIR+self.new_logidoc_path+_PK.suf_index_dir+"\n"
        elif line.__contains__(_PK.STORE_1_DIR):
            return _PK.STORE_1_DIR+self.new_logidoc_path+_PK.suf_store_1_dir+"\n"
        else:
            return line

    def run(self):
        self.log.info("start altering %s" % self.f)
        if self.f.endswith("build.properties"):
            self.__alter_build()
        elif self.f.endswith("context.properties"):
            self.__alter_context()

    def set_logger(self, logger: LogicalDocLogger):
        """set logger for this class
        :param logger:
        :return: None
        """
        self.log = logger
