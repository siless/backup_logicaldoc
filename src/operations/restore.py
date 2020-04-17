import shutil
import sys
from pathlib import Path

from src.lib.properties_reader import ReadProperties
from src.lib.variables import PathVariables, SearchForPattern
from src.lib.xml_reader import ReadXML
from src.operations.base import BasicOperations


class Restore(BasicOperations):

    def __init__(self, logger):
        """Contructor
        :param logger:  logger-object
        """
        super().__init__(logger)
        self.log.info("Start restoring")
        self.decompress_path = None

    def run(self):
        self.tar_path = self.__check_backup()  # override it from base.py bc it is containing the path and the filename as path.obj now
        self.tar_archive = self._get_tarfile_object('r')
        self.__decompress_archive()

        dumpfile = self.__search_for_in_decompress_folder(SearchForPattern.LOGICALDOC_SQL.__str__())
        docs_folder = self.__search_for_in_decompress_folder(SearchForPattern.DOCS.__str__())
        index_folder = self.__search_for_in_decompress_folder(SearchForPattern.INDEX.__str__())
        conf_folder = self.__search_for_in_decompress_folder(
            SearchForPattern.CONF.__str__()).parent  # bc we need the folder not a path with a file

        for file in ["build.properties", "context.properties"]:
            prop = ReadProperties(conf_folder.joinpath(file), self.logicaldoc_root)
            prop.set_logger(self.log)
            prop.run()

        log_xml = ReadXML(conf_folder.joinpath("log.xml"), self.logicaldoc_root)
        log_xml.set_logger(self.log)
        log_xml.run()

        # TODO code unterhalb wieder aktivieren wenn dateianpassung vollstaendig getestet ist.
        # if self._is_logicaldoc_running():
        #     out = self.run_linux_command(CLICommands.LOGICALDOC_STOP.__str__())
        #     self.log.debug("response from %s: %s" % (CLICommands.LOGICALDOC_STOP.__str__(), out))

        # self.run_linux_command(self.__get_restore_cmd(dumpfile))

        # self.__del_decompress_folders()
        # self.run_linux_command(CLICommands.LOGICALDOC_START.__str__())

    def __get_restore_cmd(self, dumpfile: Path) -> str:
        """Methode creates dumpfile command.
        :param dumpfile: sqldump-File
        :return: complete restore command
        """
        self.cfg.run()
        return "mysql -u%s -p%s %s < " + str(dumpfile) % (
            self.cfg.get_username(), self.cfg.get_password(), self.cfg.get_database())

    def __check_backup(self) -> Path:
        """Method checks if archives are available -> yes -> it displays all archives.
        :return: path-object of selected archive
        """
        backup_folder = self.cwd.joinpath(PathVariables.SRC_BACKUP.__str__())
        archives = list(backup_folder.glob("*.tar"))
        if archives.__len__() == 0:
            sys.exit("No backups available")
        else:
            for f in range(archives.__len__()):
                print(archives[f])
            while True:
                value = input("Which backup do you want to restore: ")
                for f in archives:
                    if str(f).__contains__(value):
                        return f
                else:
                    print("Wrong input")

    def __decompress_archive(self):
        """Methode decompresses tar archive to a certain folder.
        :return: None
        """
        self.decompress_path = self.cwd.joinpath(PathVariables.SRC__DECOMPRESSED.__str__())
        self.log.debug("decompress tar to %s: " % self.decompress_path)

        self.tar_archive.extractall(self.cwd.joinpath(PathVariables.SRC__DECOMPRESSED.__str__()))
        self.tar_archive.close()

    def __search_for_in_decompress_folder(self, value) -> Path:
        """Method searches for value in the decompressed tar folder.
        :param value: pattern
        :return: found path
        """
        retval = Path(self.decompress_path)
        found_values = list()

        for path in retval.rglob(value):
            found_values.append(path)

        if found_values.__len__() > 1:
            self.log.debug("searched %s found in %s" % (value, found_values))
            sys.exit("search in decompress folder found to many files. see restore.log")

        return Path(found_values[0])

    def __del_decompress_folders(self):
        """Method removes the decompressed tar´s folder.
        :return: None
        """
        shutil.rmtree(self.decompress_path)  # TODO maybe ignore_errors = True
        self.log.info("%s was deleted" % self.decompress_path)
