#!/usr/bin/env python3
import sys

from src.lib.logger import LogicalDocLogger
from src.operations.backup import Backup

from src.operations.install import Install
from src.operations.restore import Restore


def operation_ends(value):
    sys.exit("%s beendet" % value)


def __backup():
    logger = LogicalDocLogger("backup.log")
    backup = Backup(logger)
    backup.run_backup()

    operation_ends("backup")


def __restore():
    logger = LogicalDocLogger("restore.log")
    restore = Restore(logger)

    operation_ends("restore")


def __install():
    logger = LogicalDocLogger("install.log")
    while True:
        input_value = input("System wird neu installiert und alte Daten ueberschreiben [y/n]: ")
        if input_value.lower().__eq__("y"):
            install = Install(logger)

            operation_ends("Installation")
        else:
            sys.exit("Installation abgebrochen")


def main():
    # if os.getuid() != 0:
    #     sys.exit("Unzureichende Privilegien")
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
    print("Diese Anwendung verwaltet die Sicherung oder Wiederherstellung fuer logicdoc")
    main()