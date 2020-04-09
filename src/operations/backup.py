#!/usr/bin/env python3
import sys
import tempfile
import tarfile
from pathlib import Path

from src.lib.logger import LogicalDocLogger
from src.lib.variables import PathVariables, CLICommands
from src.operations.base import BasicOperations


class Backup(BasicOperations):

    dump_cmd: str
    backup: Path

    def __init__(self, logger: LogicalDocLogger):
        super().__init__(logger)
        self.backup = self.cwd.joinpath(PathVariables.SRC_BACKUP.__str__())
        self.log.info("Sicherung begonnen und wird gespeichert nach %s" % self.backup)
        self.dump_cmd = "mysqldump -u cibo -p --add-drop-database logicaldoc"
        self.log.debug("cwd: %s" % self.cwd)

    def run_backup(self) -> bool:
        """
        Methode fuehrt alle backup-Operation durch und soll als einzige Methode von aussen genutzt werden
        :return: true - wenn alle Daten gesichert werden konnten
        """
        value = self._is_logicaldoc_running()
        self.log.debug("logicaldocd is running: %s" % value)
        if value:
            out = self.run_linux_command(CLICommands.LOGICALDOC_STOP.__str__())
            self.log.debug("Rueckmeldung von %s: %s" % (CLICommands.LOGICALDOC_STOP.__str__(), out))

        self.__backup_datafiles()
        out = self.run_linux_command(CLICommands.LOGICALDOC_START.__str__())
        self.log.debug("Rueckmeldung von %s: %s" % (CLICommands.LOGICALDOC_START.__str__(), out))
        return True

    def __backup_datafiles(self):
        for x in [self.logicaldoc_conf, self.logicaldoc_doc, self.logicaldoc_index]:
            if not x.exists():
                self.log.debug("%s ist zum Sichern nicht vorhanden. Sicherung abgebrochen" % x)
                sys.exit()
        sql_dump_path = self.cwd.joinpath(PathVariables.SRC__DUMP.__str__())
        self.log.debug("dumpfile: %s" % sql_dump_path)

        try:
            with open(str(sql_dump_path), 'w')as sql:
                sql.write(self.run_linux_command(self.dump_cmd).__str__())
        except Exception:
            self.log.debug("sql dump konnte nicht durchgefuhert werden. Sicherung abgebrochen")
            sys.exit()

        self.tar_archive.add(str(sql_dump_path))
        self.tar_archive.add(str(self.logicaldoc_conf))
        self.tar_archive.add(str(self.logicaldoc_doc))
        self.tar_archive.add(str(self.logicaldoc_index))
        self.tar_archive.close()

