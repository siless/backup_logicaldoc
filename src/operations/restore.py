from pathlib import Path

from src.operations.base import BasicOperations


class Restore(BasicOperations):

    def __init__(self, logger):
        super().__init__(logger)
        self.log.info("Wiederherstellung begonnen")

    def __set_restore_cmd(self, dumpfile: Path):
        """
        Methode setzt das Kommando zum Wiederherstellen der Datenbank
        :param dumpfile: sqldump-File
        :return: None
        """
        self.restore_cmd = "mysql -u cibo -p logicaldoc < " + str(dumpfile)