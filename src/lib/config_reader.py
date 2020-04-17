import sys
from configparser import ConfigParser
from pathlib import Path

from src.lib.variables import PathVariables


class ReadConfig:

    def __init__(self):
        self.section_db, self.section_logging = None, None
        self.parser = ConfigParser()

    def run(self) -> None:
        """Method reads data from backup.ini and section[db].
        :return: None
        """
        fconfig = PathVariables.BACKUP_CONF.__str__()
        if not Path(fconfig).exists():
            sys.exit("%s does not exist. Further actions aborted")
        self.parser.read(fconfig)
        self.section_db = self.parser['db']
        self.section_logging = self.parser['logging']

    def get_host(self):
        return self.section_db['host']

    def get_username(self):
        return self.section_db['username']

    def get_password(self):
        return self.section_db['password']

    def get_database(self):
        return self.section_db['database']

    def get_logging_level(self):
        return self.section_logging['level']
