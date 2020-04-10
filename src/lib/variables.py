from enum import Enum
from pathlib import Path


def _set_archive_name(fname, fmt='%Y%m%d-%H%M%S_{fname}'):
    """
    Methode setzt ein Zeitstempel vor den Dateinamen um bestehende Archive nicht zu ueberschreiben
    :param fname: Dateiname mit Endung
    :param fmt: Format - kann abweichend sein
    :return: xxxxx_fname
    """
    import datetime
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


class PathVariables(Enum):
    """
    Enum stellt alle Variablen zur Verfuegung damit nur an einer Stelle str erstellt und geaendert werden muesssen
    """
    SRC = "src"
    SRC_BACKUP = SRC + "/backup/"
    SRC_LOGS = SRC + "/logs/"
    OPT___COMMUNITY = "/opt/logicaldoc/community]"
    SRC__DUMP = SRC_BACKUP + "logicaldoc.sql"
    SRC__TAR = SRC_BACKUP + _set_archive_name("archive.tar")
    ########################
    CONF = "conf"
    DOC = "repository/docs"
    INDEX = "repository/index"
    BACKUP_CONF = Path.cwd().joinpath(SRC.__str__(), "conf", "backup.ini")

    def __str__(self):
        return str(self.value)


class CLICommands(Enum):
    """
    Enum mit allen Kommandozeilenkommandos um keine str im Code vertreut fest eingetragen zu haben
    """
    LOGICALDOC_STATUS = "systemctl status logicaldocd"
    LOGICALDOC_START = "systemctl start logicaldocd"
    LOGICALDOC_STOP = "systemctl stop logicaldocd"

    def __str__(self):
        return str(self.value)
