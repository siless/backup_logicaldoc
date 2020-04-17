import unittest
from pathlib import Path

from src.lib.logger import LogicalDocLogger
from src.lib.properties_reader import ReadProperties


class MyTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_build_properties(self):
        log = LogicalDocLogger("test.log")
        parser = ReadProperties(Path("ressources/opt/logidoc/community/conf/build.properties"),
                                Path("/opt/logicaldoc/community"))
        parser.set_logger(log)
        parser.run()

        altered_text = "# This must be fixed with your installation path!!\nlogicaldoc.home=/opt/logicaldoc/community\n\n# This must be fixed with your service name!!\ntomcat.service=\n\ntomcat.dir=${logicaldoc.home}/tomcat\n\ntmp.dir=${logicaldoc.home}/tmp\nconf.dir=${logicaldoc.home}/conf\n\nupdate.dir=${logicaldoc.home}/updates\nupdate.workdir=${logicaldoc.home}/updates/tmp\nupdate.prefix=ldocce_upd\nupdate.updatedb=true\n\npatch.dir=${logicaldoc.home}/patches\npatch.workdir=${logicaldoc.home}/patches/tmp\npatch.prefix=ldocce_patch\nwebapp.dir=${tomcat.dir}/webapps/ROOT"

        with open("ressources/opt/logidoc/community/conf/build.properties") as prop:
            print(prop.read(), altered_text)
            self.assertEqual(prop.read(), altered_text)

    def test_context_properties(self):
        log = LogicalDocLogger("test.log")
        parser = ReadProperties(Path("ressources/opt/logidoc/community/conf/context.properties"), Path("/opt/logicaldoc/community"))
        parser.set_logger(log)
        parser.run()


if __name__ == '__main__':
    unittest.main()
