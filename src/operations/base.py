#!/usr/bin/env python3
import shlex
import shutil
import subprocess
import tarfile
from pathlib import Path
from tarfile import TarFile

from src.lib.logger import LogicalDocLogger
from src.lib.variables import PathVariables, CLICommands


class BasicOperations:
    logicaldoc_conf: Path
    logicaldoc_root: Path
    log: LogicalDocLogger

    def __init__(self, logger):
        self.dump_cmd, self.restore_cmd = None, None
        self.log = logger
        self.logicaldoc_root = self.__set_logicaldoc_root()
        self.cwd = Path().cwd()
        self.logicaldoc_conf = self.__get_conf()
        self.logicaldoc_doc = self.__get_doc()
        self.logicaldoc_index = self.__get_index()
        self.tarpath = self.__get_tarfile()
        self.tar_archive = self.__get_tarfile_object()

    def _is_logicaldoc_running(self) -> bool:
        """
        Prueft ob der logicaldocd -Dienst laeuft
        :return: true/false
        """
        if self.run_linux_command(CLICommands.LOGICALDOC_STATUS.__str__()).__contains__(b"Active: active (running)"):
            return True
        else:
            return False

    def __set_logicaldoc_root(self) -> Path:
        """
        Methode setzt den Arbeitspfad in dem logicaldoc gespeichert ist
        :return: root-Path von logicaldoc
        """
        ret = input("Installationsverzeichnis logicaldoc [/opt/logicaldoc/community]: ")
        if ret.strip().__len__() == 0:
            root = Path(PathVariables.OPT___COMMUNITY.__str__())
        else:
            root = Path(ret)

        while True:
            if not root.exists():
                root = Path(input("Verzeichnis existiert nicht: "))
            else:
                break
        self.log.info("Logicaldoc root %s" % root)
        return root

    def run_linux_command(self, cmd: str) -> bytes:
        """
        Methode fuehrt das uebergebene Linuxkommando aus
        :param cmd: Befehl
        :return: stdout
        """
        command = shlex.split(cmd)
        self.log.debug("Kommando %s wird ausgefuehrt" % cmd)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        out = proc.communicate()[0]  # nur in [0] steht die Antwort. [1] ist meinst None
        return out

    def __get_tarfile(self) -> Path:
        tarfile = self.cwd.joinpath(PathVariables.SRC__TAR.__str__())
        self.log.debug("tarfile: %s" % tarfile)
        return Path(tarfile)

    def __get_conf(self) -> Path:
        ret = self.logicaldoc_root.joinpath(PathVariables.CONF.__str__())
        self.log.debug("conf Pfad: %s" % ret)
        return ret

    def __get_doc(self) -> Path:
        ret = self.logicaldoc_root.joinpath(PathVariables.DOC.__str__())
        self.log.debug("docs Pfad: %s" % ret)
        return ret

    def __get_index(self) -> Path:
        ret = self.logicaldoc_root.joinpath(PathVariables.INDEX.__str__())
        self.log.debug("index Pfad: %s" % ret)
        return ret

    def __get_tarfile_object(self) -> TarFile:
        return tarfile.TarFile(self.tarpath, mode='w')
