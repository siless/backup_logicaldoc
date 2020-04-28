#!/usr/bin/env python3
import shlex
import subprocess
import tarfile
from pathlib import Path
from tarfile import TarFile

from src.lib.config_reader import ReadConfig
from src.lib.logger import LogicalDocLogger
from src.lib.variables import PathVariables, CLICommands


class BasicOperations:

    def __init__(self, logger: LogicalDocLogger):
        """
        Contructor.
        :param logger: logger-object
        """
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
        Checks if logicaldocd runs.
        :return: true/false
        """
        out = self.run_linux_command(CLICommands.LOGICALDOC_STATUS)
        if out.__contains__(b"Active: active (running)"):
            return True
        else:
            self.log.debug("reponse logicaldocd status: %s" % out)
            return False

    def __set_logicaldoc_root(self) -> Path:
        """
        Methode assigns the working dir where logicaldoc is stored.
        :return: root-Path von logicaldoc
        """
        ret = input("Installationfolder logicaldoc [/opt/logicaldoc/community]: ")
        if ret.strip().__len__() == 0:
            root = Path(PathVariables.OPT___COMMUNITY)
        else:
            root = Path(ret)

        while True:
            if not root.exists():
                root = Path(input("Folder does not exist: "))
            else:
                break
        self.log.info("Logicaldoc root %s" % root)
        return root

    def run_linux_command(self, cmd: str, stdin=None) -> dict:
        """
        Methode runs the linux shell command.
        Popen or run cannot interpret a redirect char e.g. '<', '>' therefore it is crucial to use the stdin-Argument
        to avoid using the shell=True option
        :param stdin: sql dump filename
        :param cmd: command
        :return: stdout or stderr
        """
        command = shlex.split(cmd)
        self.log.debug("Running command %s" % cmd)
        if stdin is None:
            proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        else:
            with open(stdin) as dump:
                proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=dump, check=True)
        out = proc.stdout
        err = proc.stderr
        self.log.debug("Process output: %s" % out.decode("utf-8"))
        self.log.debug("Process error: %s" % err.decode("utf-8"))
        return {
            'stdout': out,
            'stderr': err
        }

    def __get_tarfile(self) -> Path:
        """Get object of the backup-archive.
        :return: path-ojbect of tar-file
        """
        tarfile = self.cwd.joinpath(PathVariables.SRC__TAR)
        self.log.debug("tarfile: %s" % tarfile)
        return Path(tarfile)

    def __get_conf(self) -> Path:
        """
        Get the conf folder.
        :return: path-object of conf folder
        """
        ret = self.logicaldoc_root.joinpath(PathVariables.CONF)
        self.log.debug("conf path: %s" % ret)
        return ret

    def __get_doc(self) -> Path:
        """
        Get the doc folder.
        :return: path-object of doc-folder
        """
        ret = self.logicaldoc_root.joinpath(PathVariables.DOC)
        self.log.debug("docs path: %s" % ret)
        return ret

    def __get_index(self) -> Path:
        """
        Get the index-folder.
        :return: path-object of index-folder
        """
        ret = self.logicaldoc_root.joinpath(PathVariables.INDEX)
        self.log.debug("index path: %s" % ret)
        return ret

    def _get_tarfile_object(self, mode: str) -> TarFile:
        """
        Get a tarfile-oject.
        :param mode: modus - r -> read , w -> write
        :return: tarfile-object
        """
        return tarfile.TarFile(self.tar_path, mode=mode)
