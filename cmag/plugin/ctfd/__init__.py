from cmag import plugin
from cmag.plugin import CMagPlugin
from cmag.plugin.option import plugin_options

from .parser import CTFdParser, CTFdParserException
from tempfile import mkdtemp

@plugin_options
class CTFdPluginOptions:
    url: str = 'https://demo.ctfd.io/'
    username: str = 'user'
    password: str = 'password'

class CTFdPlugin(CMagPlugin):

    callname = 'cmag.plugin.ctfd'
    optdef = CTFdPluginOptions

    def run(self, *args, **kwargs):
        tempdir = mkdtemp()
        parser = CTFdParser(self.options.url)
        parser.login(self.options.username, self.options.password)
        for chall in parser.get_chall_list():
            challenge = self.project.add_challenge(chall['name'])
            filepath_list = parser.download_chall_files(chall['id'], tempdir)
            for filepath in filepath_list:
                challenge.add_file(filepath)