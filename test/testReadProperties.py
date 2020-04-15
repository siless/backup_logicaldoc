import unittest
from src.lib.properties_reader import ReadProperties


class MyTestCase(unittest.TestCase):
    def test_something(self):

        parser = ReadProperties("ressources/opt/logidoc/community/conf/build.properties", "/opt/logicaldoc/community")
        parser.run()

        altered_text="# This must be fixed with your installation path!!\nlogicaldoc.home=/opt/logicaldoc/community\n\n# This must be fixed with your service name!!\ntomcat.service=\n\ntomcat.dir=${logicaldoc.home}/tomcat\n\ntmp.dir=${logicaldoc.home}/tmp\nconf.dir=${logicaldoc.home}/conf\n\nupdate.dir=${logicaldoc.home}/updates\nupdate.workdir=${logicaldoc.home}/updates/tmp\nupdate.prefix=ldocce_upd\nupdate.updatedb=true\n\npatch.dir=${logicaldoc.home}/patches\npatch.workdir=${logicaldoc.home}/patches/tmp\npatch.prefix=ldocce_patch\nwebapp.dir=${tomcat.dir}/webapps/ROOT"

        with open("ressources/opt/logidoc/community/conf/build.properties") as prop:
            print(prop.read(), altered_text)
            self.assertEqual(prop.read(), altered_text)

if __name__ == '__main__':
    unittest.main()
