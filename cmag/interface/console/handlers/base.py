from __future__ import annotations

if __import__("typing").TYPE_CHECKING:
    from typing import Any, Dict, List
    from ..Session import CMagConsoleSession

import shlex
import argparse

class CMagCmdHandlerBase:

    name = ''
    usage = ''
    description = ''

    def __init__(self, session: CMagConsoleSession):
        self.session = session

    def __call__(self, arg):
        argv = self.parse_args(arg)
        if argv:
            return self.handle(argv)

    def parse_args(self, arg):

        argv = shlex.split(arg)
        parser = argparse.ArgumentParser(exit_on_error=False)
        parser.prog = self.name
        if self.usage:
            parser.usage = self.usage
        if self.description:
            parser.description = self.description
        self.create_parser(parser)

        try:
            return parser.parse_args(argv)
        except argparse.ArgumentError as e:
            return None
        except SystemExit as e:
            return None

    def create_parser(self, parser):
        return

    def handle(self, argv):
        return
