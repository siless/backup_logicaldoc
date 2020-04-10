import sys
from configparser import ConfigParser
from pathlib import Path

from src.lib.variables import PathVariables


class ReadConfig:

    def __init__(self, logger):
        self.log = logger
        self.section_db = None
        self.parser = ConfigParser()

    def run(self) -> None:
        '''
        Methode liest die Daten aus der backup.ini und die section['db]
        :return: None
        '''
        fconfig = PathVariables.BACKUP_CONF.__str__()
        if not Path(fconfig).exists():
            self.log.debug("%s does not exist")
            sys.exit()
        self.parser.read(fconfig)
        self.section_db = self.parser['db']

    def get_host(self):
        return self.section_db['host']

    def get_username(self):
        return self.section_db['username']

    def get_password(self):
        return self.section_db['password']

    def get_database(self):
        return self.section_db['database']
