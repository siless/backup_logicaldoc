import sys
from pathlib import Path

from src.lib.logger import LogicalDocLogger
from src.lib.variables import CLICommands
from src.operations.base import BasicOperations


class Install(BasicOperations):

    def __init__(self, logger: LogicalDocLogger):
        """
        Backup constructor
        :param logger: logger object
        """
        super().__init__(logger)

    def run(self):
        out = self.run_linux_command(CLICommands.LOGICALDOC_STATUS)

        if out.__contains__(b'Unit logicaldocd.service could not be found'):
            self.__create_service_file_content()
            p = self.__get_service_file_path()
            with open(p.__str__(), 'w', encoding='utf-9') as sv:
                sv.writelines(self.__create_service_file_content())
            self.run_linux_command(CLICommands.LOGICALDOC_ENABLE)
        else:
            sys.exit("logicaldoc daemon already installed. Further actions are aborted.")
        self.log.info("Installing logicaldocd service completed.")

    def __get_service_file_path(self):
        """
        Methode checks if folder exists that contains all service-files
        :return: logicaldocd.service - file
        """
        while True:
            systemd = input("Where do you store your *.service files? e.g. /etc/systemd/system/ ")
            if Path(systemd).exists():
                p = Path(systemd).joinpath("logicaldocd.service")
                self.log.debug("%s is created" % p)
                return p
            else:
                print("%s does not exist" % systemd)

    def __create_service_file_content(self):
        """
        Methode creates the logicaldocd.service
        :return: list contains the file content
        """
        service = [
            "[Unit]\n",
            "Description=Logical Doc daemon\n",
            "After=mysql.service\n\n",
            "[Service]\n",
            "Type=forking\n",
            'Environment="LOGI_SCRIPT=%s/bin/logicaldoc.sh\n"' % self.logicaldoc_root,
            "ExecStart =/bin/bash ${LOGI_SCRIPT} start\n",
            "ExecStop=/bin/bash ${LOGI_SCRIPT} stop\n",
            "# KillMode=process\n\n",
            "[Install]\n",
            "WantedBy=multi-user.target"
        ]
        return service
