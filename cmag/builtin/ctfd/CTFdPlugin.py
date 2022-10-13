from cmag import plugin
from cmag.plugin import CMagPlugin
from cmag.plugin.option import plugin_options

from .parser import CTFdNonceNotFound, CTFdParser, CTFdRequestException
from tempfile import mkdtemp

import sys

@plugin_options
class CTFdPluginOptions:
    url: str = ''
    username: str = ''
    password: str = ''

class CTFdPlugin(CMagPlugin):

    callname = 'CTFdFeeder'
    optdef = CTFdPluginOptions

    def run(self, *args, **kwargs):

        if not self.check():
            return False

        return self.main(**self.options.to_dict())

    def check(self):

        if self.options.url == '':
            self.log.error("option 'url' not set.")
            return False

        if self.options.username == '':
            self.log.error("option 'username' not set.")
            return False

        if self.options.password == '':
            self.log.error("option 'password' not set.")
            return False

        return True

    def main(self, url='', username='', password='') -> bool:

        challenge_manager = self.project.challenge_manager

        tempdir = mkdtemp()

        ctfd_parser = CTFdParser(url)

        try:
            ctfd_parser.login(username, password)
        except CTFdRequestException:
            self.log.error("failed to connect server.")
        except CTFdNonceNotFound:
            self.log.critical("CTFd server is not compatible.")
    
        if not ctfd_parser.loggedin:
            self.log.error("login failed.")
            return False

        try:
            challenge_list = ctfd_parser.get_chall_list()
            self.log.info(f"Total {len(challenge_list)} challenges.")
            for chall in challenge_list:
                challenge = challenge_manager.add_challenge(chall['name'])
                self.log.info(f"Downloading files of challenge {chall['name']}...")
                filepath_list = ctfd_parser.download_chall_files(chall['id'], tempdir)
                self.log.info(f"{len(filepath_list)} files downloaded.")
                for filepath in filepath_list:
                    challenge.add_file(filepath)
                    
        except CTFdRequestException:
            self.log.error("failed to connect server.")
            return False

        return True