#!/usr/bin/env python3
import logging

from src.lib.config_reader import ReadConfig
from src.lib.variables import PathVariables


class LogicalDocLogger:

    def __init__(self, logfile: str):
        """
        :param xxx.log
        """
        # cfg = ReadConfig()
        # cfg.run()
        #TODO level=cfg.get_logging_level() zum laufen bringen da basicConfig den wert nicht akzeptiert
        logging.basicConfig(filename=PathVariables.SRC_LOGS.__str__()+logfile, format=self.__get_format(), level=logging.DEBUG)

    def info(self, msg: str):
        logging.info(msg)

    def debug(self, msg: str):
        logging.debug(msg)

    def warn(self, msg: str):
        logging.warning(msg)

    def __get_format(self) -> str:
        return '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
