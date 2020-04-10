import sys
from pathlib import Path

from src.lib.variables import PathVariables
from src.operations.base import BasicOperations


class Restore(BasicOperations):

    def __init__(self, logger):
        super().__init__(logger)
        self.log.info("Start restoring")

    def run(self):
        self.cfg.run()
        self.__check_backup()

    def __set_restore_cmd(self, dumpfile: Path):
        """
        Methode setzt das Kommando zum Wiederherstellen der Datenbank
        :param dumpfile: sqldump-File
        :return: None
        """
        self.restore_cmd = "mysql -u cibo -p logicaldoc < " + str(dumpfile)

    def __check_backup(self):
        backup_folder = self.cwd.joinpath(PathVariables.SRC_BACKUP.__str__())
        archives = list(backup_folder.glob("*.tar"))
        if archives.__len__() == 0:
            sys.exit("No backups available")
        else:
            for f in range(archives.__len__()):
                print(archives[f])
            while True:
                value = input("Which backkup do you want to restore: ")
                for f in archives:
                    if str(f).__contains__(value):
                        break
                #TODO abbruch der schleife richtig verarbeiten und beenden. im archive sind die pfade als posix(....) angegeben 
                else:
                    print("Wrong input")
                    print(archives)


