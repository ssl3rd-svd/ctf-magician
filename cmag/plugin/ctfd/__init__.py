from cmag import plugin
from cmag.plugin import CMagPlugin
from cmag.plugin.option import plugin_options

from .parser import CTFdParser, CTFdParserException
from tempfile import mkdtemp

import sys

@plugin_options
class CTFdPluginOptions:
    url: str = ''
    username: str = ''
    password: str = ''

class CTFdPlugin(CMagPlugin):

    callname = 'cmag.plugin.ctfd'
    optdef = CTFdPluginOptions

    def run(self, *args, **kwargs):

        check, message = self.check()
        if not check:
            self.log.error(message)
            return False

        return self.main(**self.options.to_dict())

    def check(self):
        if self.options.url == '':
            return (False, "option 'url' not set.")
        if self.options.username == '':
            return (False, "option 'username' not set.")
        if self.options.password == '':
            return (False, "option 'password' not set.")
        return (True, 'success')

    def main(self, url='', username='', password=''):
        challenge_manager = self.project.challenge_manager
        tempdir = mkdtemp()
        parser = CTFdParser(url)
        parser.login(username, password)
        for chall in parser.get_chall_list():
            challenge = challenge_manager.add_challenge(chall['name'])
            filepath_list = parser.download_chall_files(chall['id'], tempdir)
            for filepath in filepath_list:
                challenge.add_file(filepath)