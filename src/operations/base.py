#!/usr/bin/env python3
import shlex
import shutil
import subprocess
import tarfile
from pathlib import Path
from tarfile import TarFile

from src.lib.config_reader import ReadConfig
from src.lib.logger import LogicalDocLogger
from src.lib.variables import PathVariables, CLICommands


class BasicOperations:
    logicaldoc_conf: Path
    logicaldoc_root: Path
    log: LogicalDocLogger

    def __init__(self, logger):
        self.tar_archive = None, None, None
        self.log = logger
        self.logicaldoc_root = self.__set_logicaldoc_root()
        self.cwd = Path().cwd()
        self.logicaldoc_conf = self.__get_conf()
        self.logicaldoc_doc = self.__get_doc()
        self.logicaldoc_index = self.__get_index()
        self.tar_path = self.__get_tarfile()
        self.cfg = ReadConfig()

    def run(self):
        raise NotImplementedError("method not implemented")

    def _is_logicaldoc_running(self) -> bool:
        """
        Checks if logicaldocd runs
        :return: true/false
        """
        if self.run_linux_command(CLICommands.LOGICALDOC_STATUS.__str__()).__contains__(b"Active: active (running)"):
            return True
        else:
            return False

    def __set_logicaldoc_root(self) -> Path:
        """
        Methode assigns the working dir where logicaldoc is stored
        :return: root-Path von logicaldoc
        """
        ret = input("Installationfolder logicaldoc [/opt/logicaldoc/community]: ")
        if ret.strip().__len__() == 0:
            root = Path(PathVariables.OPT___COMMUNITY.__str__())
        else:
            root = Path(ret)

        while True:
            if not root.exists():
                root = Path(input("Folder does not exist: "))
            else:
                break
        self.log.info("Logicaldoc root %s" % root)
        return root

    def run_linux_command(self, cmd: str) -> bytes:
        """
        Methode runs the linux shell command
        :param cmd: command
        :return: stdout
        """
        command = shlex.split(cmd)
        self.log.debug("Running command %s" % cmd)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        out = proc.communicate()[0]  # nur in [0] steht die Antwort. [1] ist meinst None
        return out

    def __get_tarfile(self) -> Path:
        """
        Get object of the backup-archive
        :return: path-ojbect of tar-file
        """
        tarfile = self.cwd.joinpath(PathVariables.SRC__TAR.__str__())
        self.log.debug("tarfile: %s" % tarfile)
        return Path(tarfile)

    def __get_conf(self) -> Path:
        """
        Get the conf folder
        :return: path-object of conf folder
        """
        ret = self.logicaldoc_root.joinpath(PathVariables.CONF.__str__())
        self.log.debug("conf path: %s" % ret)
        return ret

    def __get_doc(self) -> Path:
        """
        Get the doc folder
        :return: path-object of doc-folder
        """
        ret = self.logicaldoc_root.joinpath(PathVariables.DOC.__str__())
        self.log.debug("docs path: %s" % ret)
        return ret

    def __get_index(self) -> Path:
        """
        Get the the index-folder
        :return: path-object of index-folder
        """
        ret = self.logicaldoc_root.joinpath(PathVariables.INDEX.__str__())
        self.log.debug("index path: %s" % ret)
        return ret

    def _get_tarfile_object(self, mode: str) -> TarFile:
        """
        Get a tarfile-oject
        :param mode: modus - r -> read , w -> write
        :return: tarfile-object
        """
        return tarfile.TarFile(self.tar_path, mode=mode)
