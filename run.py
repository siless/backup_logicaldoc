#!/usr/bin/env python3
import os
import sys

from src.lib.logger import LogicalDocLogger
from src.operations.backup import Backup
from src.operations.install import Install
from src.operations.restore import Restore


def operation_ends(value):
    sys.exit("%s beendet" % value)


def __backup():
    logger = LogicalDocLogger("backup.log").get_prepared_logger()
    backup = Backup(logger)
    backup.run()

    operation_ends("backup")


def __restore():
    logger = LogicalDocLogger("restore.log").get_prepared_logger()
    restore = Restore(logger)
    restore.run()

    operation_ends("restore")


def __install():
    logger = LogicalDocLogger("install.log").get_prepared_logger()
    install = Install(logger)
    install.run()

    operation_ends("Installation")


def main():
    print("This application manages restoring and backup up for logicaldoc community")
    while True:
        value = input("[backup|restore|install] ")
        value = value.strip()
        if value.lower().__eq__("backup"):
            __backup()
        elif value.lower().__eq__("restore"):
            __restore()
        elif value.lower().__eq__("install"):
            __install()


if __name__ == '__main__':
    if os.getuid() != 0:
        sys.exit("Unzureichende Privilegien")
    main()
