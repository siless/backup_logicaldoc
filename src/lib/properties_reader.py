from pathlib import Path
from configparser import ConfigParser

from src.lib.variables import PropertiesKeys


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

        #path suffixes that are added to self.logicaldoc_root
        suf_acmecad_command = "acmecad/AcmeCADConverter.exe"
        suf_acmedad_resource = "acmecad/logicaldoc.ini"
        suf_conf_dbdir = "repository/db/"
        suf_conf_exportdir = "repository/impex/out/"
        sufconf_importdir = "repository/impex/in/"
        suf_conf_logdir = "repository/logs/"
        suf_conf_plugindir = "repository/plugins/"
        suf_conf_userdir = "repository/users/"
        suf_index_dir = "repository/index/"
        suf_store_1_dir = "repository/docs/"

    def __alter_build(self):
        """Method alters values in build.properties
        :return: None
        """
        with open(self.f, 'r') as prop:
            tmp = list()
            for line in prop.readlines():
                if line.__contains__(PropertiesKeys.LOGICALDOC_HOME.__str__()):
                    self.log.debug("altered %s to %s" % (line, self.new_logidoc_path))
                    tmp.append(PropertiesKeys.LOGICALDOC_HOME.__str__() + self.new_logidoc_path+"\n")
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
                # TODO context.properties anpassen
                pass

        pass

    def run(self):
        self.log.info("start altering %s" % self.f)
        if self.f.endswith("build.properties"):
            self.__alter_build()
        elif self.f.endswith("context.properties"):
            self.__alter_context()

    def set_logger(self, logger):
        self.log = logger