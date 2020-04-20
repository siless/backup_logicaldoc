from src.lib.logger import LogicalDocLogger
from src.operations.base import BasicOperations


class Install(BasicOperations):

    def __init__(self, logger: LogicalDocLogger):
        """
        Backup constructor
        :param logger: logger object
        """
        super().__init__(logger)

    def run(self):
        pass
