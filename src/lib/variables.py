from enum import Enum
from pathlib import Path


def _set_archive_name(fname, fmt='%Y%m%d-%H%M%S_{fname}'):
    """
    Method adds a timestamp as a prefix to the tar archives.
    :param fname: filename with suffix e.g. archive.tar
    :param fmt: personal own format
    :return: xxxxx_fname
    """
    import datetime
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


class PathVariables(Enum):
    """
    Enum offers str-vars , that the modules does not need any further str-vars
    """
    SRC = "src"
    SRC_BACKUP = SRC + "/backup/"
    SRC_LOGS = SRC + "/logs/"
    OPT___COMMUNITY = "/opt/logicaldoc/community]"
    SRC__DUMP = SRC_BACKUP + "logicaldoc.sql"
    SRC__TAR = SRC_BACKUP + _set_archive_name("archive.tar")
    SRC__DECOMPRESSED = SRC_BACKUP + "/decompressed/"
    ########################
    CONF = "conf"
    DOC = "repository/docs"
    INDEX = "repository/index"
    BACKUP_CONF = Path.cwd().joinpath(SRC.__str__(), "conf", "backup.ini")

    def __str__(self):
        return str(self.value)


class CLICommands(Enum):
    """
    Enum with all linux commands.
    """
    LOGICALDOC_STATUS = "systemctl status logicaldocd"
    LOGICALDOC_START = "systemctl start logicaldocd"
    LOGICALDOC_STOP = "systemctl stop logicaldocd"

    def __str__(self):
        return str(self.value)


class SearchForPattern(Enum):
    """
    Enum that contains search pattern for e.g. shutils.glob()
    """
    LOGICALDOC_SQL = "logicaldoc.sql"
    INDEX = "repository/index/"
    DOCS = "repository/docs/"
    CONF = "conf/context.properties"

    def __str__(self):
        return str(self.value)


class PropertiesKeys(Enum):
    """
    Enum that contains the keys of the property files build.properties and context.properties that must be altered at a restore
    """
    LOGICALDOC_HOME = "logicaldoc.home="
    LDOCHOME = "LDOCHOME="
    ACMECAD_COMMAND = "acmecad.command=" #acmecad/AcmeCADConverter.exe
    ACMEDAD_RESOURCE = "acmecad.resource=" #acmecad/logicaldoc.ini
    CONF_DBDIR = "conf.dbdir=" #repository/db/
    CONF_EXPORTDIR = "conf.exportdir=" #repository/impex/out/
    CONF_IMPORTDIR = "conf.importdir=" #repository/impex/in/
    CONF_LOGDIR = "conf.logdir=" #repository/logs/
    CONF_PLUGINDIR = "conf.plugindir=" #repository/plugins/
    CONF_USERDIR = "conf.userdir=" #repository/users/
    INDEX_DIR = "index.dir=" #repository/index/
    STORE_1_DIR = "store.1.dir=" #repository/docs/


    def __str__(self):
        return str(self.value)
