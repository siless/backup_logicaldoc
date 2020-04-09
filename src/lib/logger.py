#!/usr/bin/env python3
import logging

from src.lib.variables import PathVariables


class LogicalDocLogger:

    def __init__(self, logfile: str):
        """
        :param xxx.log
        """
        info = logging.INFO
        debug = logging.DEBUG
        logging.basicConfig(filename=PathVariables.SRC_LOGS.__str__()+logfile, format=self.__get_format(), level=debug)

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)

    def warn(self, msg):
        logging.warning(msg)

    def __get_format(self) -> str:
        return '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
