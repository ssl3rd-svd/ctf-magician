from .Session import CMagConsoleSession
from .handlers import *

from cmd import Cmd
from colorama import init
from termcolor import colored

class CMagConsole(Cmd):

    prompt_cursor = colored('\n> ', color='magenta', attrs=['bold'])
    prompt = prompt_cursor

    def __init__(self, session: CMagConsoleSession,
                       *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session

    def emptyline(self) -> bool:
        return False

    def postcmd(self, stop: bool, line: str) -> bool:

        if self.session.project != None:
            if self.session.challenge == None:
                self.prompt  = '\n'
                self.prompt += colored(self.session.project.dir, color='cyan')
                self.prompt += self.prompt_cursor
            else:
                self.prompt  = '\n'
                self.prompt += colored(self.session.project.dir, color='cyan') 
                self.prompt += ' '
                self.prompt += colored(str(self.session.challenge.id), color='grey')
                self.prompt += self.prompt_cursor
        else:
            self.prompt = self.prompt_cursor

        return super().postcmd(stop, line)

    def do_exit(self, arg):
        'Exit CTF-Magician console.'
        return True

def add_console_args(parser, subparsers):
    cui_parser = subparsers.add_parser('cui')
    cui_parser.set_defaults(func=console_main)
    return cui_parser

def console_main(args):

    session = CMagConsoleSession(
        CMagConsole,
        [CMagCmdProjectHandler]
    )

    try:
        init()
        session.console.cmdloop()
    except KeyboardInterrupt:
        session.console.do_exit(None)
