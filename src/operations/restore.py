import shutil
import sys
from pathlib import Path

from src.lib.properties_reader import ReadProperties
from src.lib.variables import PathVariables, SearchForPattern, CLICommands
from src.lib.xml_reader import ReadXML
from src.operations.base import BasicOperations


class Restore(BasicOperations):

    def __init__(self, logger):
        """
        Restore contructor.
        :param logger:  logger-object
        """
        super().__init__(logger)
        self.log.info("Start restoring")
        self.decompress_path = None

    def run(self):
        self.tar_path = self.__check_backup()  # override it from base.py bc it is containing the path and the filename as path.obj now
        self.tar_archive = self._get_tarfile_object('r')
        self.__decompress_archive()

        dumpfile = self.__search_in_decompress_folder(SearchForPattern.LOGICALDOC_SQL)
        docs_folder = self.__search_in_decompress_folder(SearchForPattern.DOCS)
        index_folder = self.__search_in_decompress_folder(SearchForPattern.INDEX)
        conf_folder = self.__search_in_decompress_folder(
            SearchForPattern.CONF).parent  # bc we need the folder not a path with a file

        self.__alter_logicaldoc_config_files(conf_folder)

        if self._is_logicaldoc_running():
            out = self.run_linux_command(CLICommands.LOGICALDOC_STOP)
            self.log.debug("response from %s: %s" % (CLICommands.LOGICALDOC_STOP, out))

        out = self.run_linux_command(self.__get_restore_cmd(dumpfile))
        self.log.debug("import mysql dump (drop database) - %s" % out)

        #copy decompressed tar and altered config files to logicaldoc home subdirs
        #first of all -> del old dirs bc copytree does not overwrite existing dirs
        for i in [self.logicaldoc_doc, self.logicaldoc_index, self.logicaldoc_conf]:
            try:
                shutil.rmtree(str(i))
                self.log.info("%s, was deleted" % (str(i)))
            except FileNotFoundError:
                self.log.debug("%s does not exist. Nothing to remove" % str(i))
        for src, dst in [(conf_folder, self.logicaldoc_conf), (index_folder, self.logicaldoc_index), (docs_folder, self.logicaldoc_doc)]:
            self.log.info("%s was copied to %s" % (str(src), str(dst)))
            shutil.copytree(str(src), str(dst))

        self.__del_decompress_folders()
        self.run_linux_command(CLICommands.LOGICALDOC_START)

    def __get_restore_cmd(self, dumpfile: Path) -> str:
        """
        Methode creates dumpfile command.
        :param dumpfile: sqldump-File
        :return: complete restore command
        """
        self.cfg.run()
        return "mysql -u%s -p%s %s < %s" % (self.cfg.get_username(), self.cfg.get_password(), self.cfg.get_database(), str(dumpfile))

    def __check_backup(self) -> Path:
        """
        Method checks if archives are available -> yes -> it displays all archives.
        :return: path-object of selected archive
        """
        backup_folder = self.cwd.joinpath(PathVariables.SRC_BACKUP.__str__())
        archives = list(backup_folder.glob("*.tar"))
        if archives.__len__() == 0:
            sys.exit("No backups available")
        else:
            for f in archives:
                print(f)
            while True:
                value = input("Which backup do you want to restore: ")
                if value.__len__() != 0:
                    for f in archives:
                        if str(f) == value:
                            return f
                    else:
                        print("Wrong input")

    def __decompress_archive(self):
        """
        Methode decompresses tar archive to a certain folder.
        :return: None
        """
        self.decompress_path = self.cwd.joinpath(PathVariables.SRC__DECOMPRESSED)
        self.log.debug("decompress tar to %s: " % self.decompress_path)

        self.tar_archive.extractall(self.cwd.joinpath(PathVariables.SRC__DECOMPRESSED))
        self.tar_archive.close()

    def __search_in_decompress_folder(self, value) -> Path:
        """
        Method searches for value in the decompressed tar folder.
        :param value: pattern
        :return: found path
        """
        retval = Path(self.decompress_path)
        found_values = list()

        for path in retval.rglob(value):
            found_values.append(path)

        if found_values.__len__() > 1:
            self.log.debug("searched %s found in %s" % (value, found_values))
            sys.exit("search in decompress folder found to many matches. see restore.log")

        return Path(found_values[0])

    def __del_decompress_folders(self):
        """
        Method removes the decompressed tar´s folder.
        :return: None
        """
        shutil.rmtree(self.decompress_path)  # TODO maybe ignore_errors = True
        self.log.info("%s was deleted" % self.decompress_path)

    def __alter_logicaldoc_config_files(self, conf_folder: Path):
        """
        Method contains the operations to alter the .xml and .properties files.
        :param conf_folder: folder of config-files
        :return: None
        """
        for file in ["build.properties", "context.properties"]:
            prop = ReadProperties(conf_folder.joinpath(file), self.logicaldoc_root)
            prop.set_logger(self.log)
            prop.run()

        log_xml = ReadXML(conf_folder.joinpath("log.xml"), self.logicaldoc_root)
        log_xml.set_logger(self.log)
        log_xml.run()
