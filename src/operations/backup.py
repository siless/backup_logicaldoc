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
        self.log.info("Back up is running and will be stored at %s" % self.backup)
        self.dump_cmd = self.__get_sql_dump()
        self.log.debug("cwd: %s" % self.cwd)
        self.tar_archive = self._get_tarfile_object('w')

    def run(self):
        """Method runs all backup-operations and offers the only access to this class
        :return: None
        """
        if self._is_logicaldoc_running():
            out = self.run_linux_command(CLICommands.LOGICALDOC_STOP.__str__())
            self.log.debug("response from %s: %s" % (CLICommands.LOGICALDOC_STOP.__str__(), out))

        self.__backup_datafiles()
        out = self.run_linux_command(CLICommands.LOGICALDOC_START.__str__())
        self.log.debug("response from %s: %s" % (CLICommands.LOGICALDOC_START.__str__(), out))

    def __backup_datafiles(self):
        """Method checks if folders which are backed up are available and creates a sql export file from mysql
        :return: None
        """
        for x in [self.logicaldoc_conf, self.logicaldoc_doc, self.logicaldoc_index]:
            if not x.exists():
                self.log.debug("%s is not available for backing up. Backup up aborted" % x)
                sys.exit()
        sql_dump_path = self.cwd.joinpath(PathVariables.SRC__DUMP.__str__())
        self.log.debug("dumpfile: %s" % sql_dump_path)

        try:
            with open(str(sql_dump_path), 'w')as sql:
                stream = self.run_linux_command(self.dump_cmd)
                sql.write(stream.decode("utf-8"))
        except Exception:
            self.log.debug("sql dump could not be executed. Backup aborted")
            sys.exit()

        self.tar_archive.add(str(sql_dump_path))
        self.tar_archive.add(str(self.logicaldoc_conf))
        self.tar_archive.add(str(self.logicaldoc_doc))
        self.tar_archive.add(str(self.logicaldoc_index))
        self.tar_archive.close()

    def __get_sql_dump(self) -> str:
        """Method creates sqldump - command
        :return: command
        """
        self.cfg.run()
        return "mysqldump -u%s -p%s --add-drop-database %s" %(self.cfg.get_username(), self.cfg.get_password(), self.cfg.get_database())