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
        cfg = ReadConfig()
        cfg.run()
        # TODO level=cfg.get_logging_level() zum laufen bringen da basicConfig den wert nicht akzeptiert
        logging.basicConfig(filename=PathVariables.SRC_LOGS + logfile, format=self.get_format(),
                            level=int(cfg.get_logging_level()))

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
