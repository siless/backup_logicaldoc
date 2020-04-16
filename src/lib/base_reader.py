from pathlib import Path

from src.lib.logger import LogicalDocLogger


class BasicReader(object):

    def __init__(self, file: Path, value: Path):
        """
        Constructor
        :param file: file to alter
        :param value: new logicaldoc-home value
        """
        self.f = str(file)
        self.new_logidoc_path = str(value)
        self.log = None

    def set_logger(self, logger: LogicalDocLogger):
        """set logger for this class
        :param logger:
        :return: None
        """
        self.log = logger

    def run(self):
        raise NotImplementedError
