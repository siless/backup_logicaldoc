from src.operations.base import BasicOperations


class Install(BasicOperations):

    def __init__(self, logger):
        super().__init__(logger)
        self.log.info("Installation begonnen")
