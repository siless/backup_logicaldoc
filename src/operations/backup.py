#!/usr/bin/env python3
import sys

from src.lib.logger import LogicalDocLogger
from src.lib.variables import PathVariables, CLICommands
from src.operations.base import BasicOperations


class Backup(BasicOperations):

    def __init__(self, logger: LogicalDocLogger):
        """
        Backup constructor
        :param logger: logger object
        """
        super().__init__(logger)
        self.backup = self.cwd.joinpath(PathVariables.SRC_BACKUP)
        self.log.info("Back up is running and will be stored at %s" % self.backup)
        self.log.debug("cwd: %s" % self.cwd)
        self.tar_archive = self._get_tarfile_object('w')

    def run(self):
        """
        Method runs all backup-operations and offers the only access to this class.
        :return: None
        """
        if self._is_logicaldoc_running():
            out = self.run_linux_command(CLICommands.LOGICALDOC_STOP)
            self.log.debug("response from %s: %s" % (CLICommands.LOGICALDOC_STOP, out))

        self.__backup_datafiles()
        out = self.run_linux_command(CLICommands.LOGICALDOC_START.__str__())
        self.log.debug("response from %s: %s" % (CLICommands.LOGICALDOC_START, out))

    def __backup_datafiles(self):
        """
        Method checks if folders which are backed up are available and creates a sql export file from mysql.
        :return: None
        """
        for x in [self.logicaldoc_conf, self.logicaldoc_doc, self.logicaldoc_index]:
            if not x.exists():
                self.log.debug("%s is not available for backing up. Backup up aborted" % x)
                sys.exit()
        sql_dump_path = self.cwd.joinpath(PathVariables.SRC__DUMP)
        self.log.debug("dumpfile: %s" % sql_dump_path)

        try:
            out = self.run_linux_command(self.__get_sql_dump_cmd())

            self.log.debug("output sql dump: %s" % out)
            # with open(str(sql_dump_path), 'w') as sql:
            #     sql.write(out.get(CLICommands.STDOUT).decode("utf-8"))
        except Exception as e:
            self.log.debug("sql dump could not be executed. Backup aborted: %s" % e)
            sys.exit()

        self.tar_archive.add(str(sql_dump_path))
        self.tar_archive.add(str(self.logicaldoc_conf))
        self.tar_archive.add(str(self.logicaldoc_doc))
        self.tar_archive.add(str(self.logicaldoc_index))
        self.tar_archive.close()

    def __get_sql_dump_cmd(self) -> str:
        """
        Method creates sqldump - command.
        :return: command
        """
        self.cfg.run()
        # return "mysqldump -u%s -p%s --add-drop-database %s >" % (self.cfg.get_username(), self.cfg.get_password(), self.cfg.get_database())
        return 'mysqldump -u%s -p%s --add-drop-database %s > %s' % (self.cfg.get_username(), self.cfg.get_password(), self.cfg.get_database(), PathVariables.SRC__DUMP)
