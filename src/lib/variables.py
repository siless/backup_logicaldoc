from enum import Enum
from pathlib import Path


def _set_archive_name(fname, fmt='%Y%m%d-%H%M%S_{fname}'):
    """Method adds a timestamp as a prefix to the tar archives.
    :param fname: filename with suffix e.g. archive.tar
    :param fmt: personal own format
    :return: xxxxx_fname
    """
    import datetime
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


class PathVariables(Enum):
    """Enum offers str-vars , that the modules does not need any further str-vars.
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
    """Enum with all linux commands.
    """
    LOGICALDOC_STATUS = "systemctl status logicaldocd"
    LOGICALDOC_START = "systemctl start logicaldocd"
    LOGICALDOC_STOP = "systemctl stop logicaldocd"

    def __str__(self):
        return str(self.value)


class SearchForPattern(Enum):
    """Enum that contains search pattern for e.g. shutils.glob().
    """
    LOGICALDOC_SQL = "logicaldoc.sql"
    INDEX = "repository/index/"
    DOCS = "repository/docs/"
    CONF = "conf/context.properties"

    def __str__(self):
        return str(self.value)


class PropertiesKeys:
    """Static class that contains the keys of the property files build.properties and context.properties that must be altered at a restore.
    """
    LOGICALDOC_HOME = "logicaldoc.home="
    LDOCHOME = "LDOCHOME="
    ACMECAD_COMMAND = "acmecad.command="  # acmecad/AcmeCADConverter.exe
    ACMEDAD_RESOURCE = "acmecad.resource="  # acmecad/logicaldoc.ini
    CONF_DBDIR = "conf.dbdir="  # repository/db/
    CONF_EXPORTDIR = "conf.exportdir="  # repository/impex/out/
    CONF_IMPORTDIR = "conf.importdir="  # repository/impex/in/
    CONF_LOGDIR = "conf.logdir="  # repository/logs/
    CONF_PLUGINDIR = "conf.plugindir="  # repository/plugins/
    CONF_USERDIR = "conf.userdir="  # repository/users/
    INDEX_DIR = "index.dir="  # repository/index/
    STORE_1_DIR = "store.1.dir="  # repository/docs/

    # path suffixes that are added to self.logicaldoc_root
    suf_acmecad_command = "/acmecad/AcmeCADConverter.exe"
    suf_acmedad_resource = "/acmecad/logicaldoc.ini"
    suf_conf_dbdir = "/repository/db/"
    suf_conf_exportdir = "/repository/impex/out/"
    suf_conf_importdir = "/repository/impex/in/"
    suf_conf_logdir = "/repository/logs/"
    suf_conf_plugindir = "/repository/plugins/"
    suf_conf_userdir = "/repository/users/"
    suf_index_dir = "/repository/index/"
    suf_store_1_dir = "/repository/docs/"


class XmlKeys:
    PARAM___FILE = "File"
    PARAM_KEY_VALUE = "value"
    __WEB = "_WEB"
    __APPENDER_DMS = "DMS"
    __APPENDER_DMS_WEB = __APPENDER_DMS + __WEB
    __APPENDER_DB = "DB"
    __APPENDER_CP = "CP"
    __APPENDER_CMIS = "CMIS"
    __APPENDER_InOp = "IndexOptimizer"
    __APPENDER_InOpWb = __APPENDER_InOp + __WEB
    __APPENDER_TaPr = "TagsProcessor"
    __APPENDER_TaPrWb = __APPENDER_TaPr + __WEB
    __APPENDER_InTa = "IndexerTask"
    __APPENDER_InTaWb = __APPENDER_InTa + __WEB
    __APPENDER_DiPr = "DigestProcessor"
    __APPENDER_DiPrWb = __APPENDER_DiPr + __WEB
    __APPENDER_PaCa = "PathCalculator"
    __APPENDER_PaCaWb = __APPENDER_PaCa + __WEB
    __APPENDER_SPRING = "spring"
    __APPENDER_AUTOMATION = "automation"

    # suffix
    __REPO_LOG = "/repository/logs/"
    __SUF_WEB = ".html"
    __suf_automation = __REPO_LOG + "automation.log"
    __suf_spring = __REPO_LOG + "spring.log"
    __suf_pa_ca = __REPO_LOG + "pathcalculator.log"
    __suf_pa_ca_wb = __suf_pa_ca + __SUF_WEB
    __suf_di_pr = __REPO_LOG + "digestprocessor.log"
    __suf_di_pr_wb = __suf_di_pr + __SUF_WEB
    __suf_in_ta = __REPO_LOG + "indexertask.log"
    __suf_in_ta_wb = __suf_in_ta + __SUF_WEB
    __suf_ta_pr = __REPO_LOG + "tagsprocessor.log"
    __suf_ta_pr_wb = __suf_ta_pr + __SUF_WEB
    __suf_in_op = __REPO_LOG + "indexoptimizer.log"
    __suf_in_op_wb = __suf_in_op + __SUF_WEB
    __suf_cmis = __REPO_LOG + "cmis.log"
    __suf_cp = __REPO_LOG + "cp.log"
    __suf_db = __REPO_LOG + "db.log"
    __suf_dms = __REPO_LOG + "dms.log"
    __suf_dms_wb = __suf_dms + __SUF_WEB

    name_value_list = [
        [__APPENDER_DMS, __suf_dms],
        [__APPENDER_DMS_WEB, __suf_dms_wb],
        [__APPENDER_DB, __suf_db],
        [__APPENDER_CP, __suf_cp],
        [__APPENDER_CMIS, __suf_cmis],
        [__APPENDER_InOp, __suf_in_op],
        [__APPENDER_InOpWb, __suf_in_op_wb],
        [__APPENDER_TaPr, __suf_ta_pr],
        [__APPENDER_TaPrWb, __suf_ta_pr_wb],
        [__APPENDER_InTa, __suf_in_ta],
        [__APPENDER_InTaWb, __suf_in_ta_wb],
        [__APPENDER_DiPr, __suf_di_pr],
        [__APPENDER_DiPrWb, __suf_di_pr_wb],
        [__APPENDER_PaCa, __suf_pa_ca],
        [__APPENDER_PaCaWb, __suf_pa_ca_wb],
        [__APPENDER_SPRING, __suf_spring],
        [__APPENDER_AUTOMATION, __suf_automation]
    ]