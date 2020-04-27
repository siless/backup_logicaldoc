#!/usr/bin/env python3
import logging

from src.lib.config_reader import ReadConfig
from src.lib.variables import PathVariables


class LogicalDocLogger(object):
    """Class offers the logging functionality."""

    def __init__(self, logfile: str):
        """
        Constructor.
        :param xxx.log
        """
        self.cfg = None
        self.logfile = logfile

    def get_prepared_logger(self):
        self.__read_ini()
        self.__build_logger()
        return self

    def __read_ini(self):
        self.cfg = ReadConfig()
        self.cfg.run()

    def __build_logger(self):
        logging.basicConfig(filename=PathVariables.SRC_LOGS + self.logfile, format=self.get_format(), level=int(self.cfg.get_logging_level()))

    @staticmethod
    def get_format() -> str:
        return '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @staticmethod
    def warning(msg: str):
        logging.warning(msg)

    @staticmethod
    def info(msg: str):
        logging.info(msg)

    @staticmethod
    def debug(msg: str):
        logging.debug(msg)
