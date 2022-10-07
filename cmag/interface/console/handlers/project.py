from __future__ import annotations

if __import__("typing").TYPE_CHECKING:
    from typing import Any, Dict, List

from argparse import ArgumentParser, Namespace
from pathlib import Path

from cmag.project import CMagProject

from .base import CMagCmdHandlerBase as handler
class CMagCmdProjectHandler(handler):
    '''project commands'''

    name = 'project'
    usage = ''
    description = ''

    def create_parser(self, parser: ArgumentParser):

        subparsers = parser.add_subparsers(dest='subcmd', required=True)

        cmd_create_parser = subparsers.add_parser('create')
        cmd_create_parser.add_argument("path")
        cmd_create_parser.add_argument("--load-config-from", type=Path)
        cmd_create_parser.set_defaults(func=self.handle_create)

        cmd_open_parser = subparsers.add_parser('open')
        cmd_open_parser.add_argument("path")
        cmd_open_parser.add_argument("--load-config-from", type=Path)
        cmd_open_parser.set_defaults(func=self.handle_open)

        cmd_close_parser = subparsers.add_parser('close')
        cmd_close_parser.add_argument("--dont-save-config", action='store_true')
        cmd_close_parser.set_defaults(func=self.handle_close)

    def handle(self, *args, **kwargs):
        if args[0] and isinstance(args[0], Namespace):
            return args[0].func(args[0])

    def handle_create(self, args: Namespace):

        if self.session.project != None:
            print("please close project first.")
            return

        self.session.project = CMagProject.create(
            args.path,
            cfg_load_file=args.load_config_from
        )

    def handle_open(self, args: Namespace):

        if self.session.project != None:
            print("please close project first.")
            return

        self.session.project = CMagProject.load(
            args.path,
            cfg_load_file=args.load_config_from
        )

    def handle_close(self, args: Namespace):

        if self.session.project == None:
            print("there are no project to close.")
            return

        if not args.dont_save_config:
            self.session.project.config.savefile()

        del self.session.project
        self.session.project = None
