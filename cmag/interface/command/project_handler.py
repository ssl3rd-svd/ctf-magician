from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Optional

from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path

# project ... {subcommand}

def project_handler(args):
    raise NotImplementedError

def project_argparse(parser: ArgumentParser):
    parser.set_defaults(func=project_handler)

# project ... create ...

def project_create_handler(args: Namespace):

    import sys
    from io import IOBase
    from cmag.project import CMagProject
    from cmag.interface.logger import CMagLogger

    log_level: int = getattr(CMagLogger, args.log_level.upper())

    if args.log_stream == 'null':
        log_stream: Optional[IOBase] = None
    else:
        log_stream: Optional[IOBase] = getattr(sys, args.log_stream)

    log_file = args.log_file

    project = CMagProject(args.project, log_level=log_level, log_to_stream=log_stream, log_to_file=log_file)
    if not project:
        print("failed.")
    else:
        print("done.")

def project_create_argparse(parser: ArgumentParser):
    parser.set_defaults(func=project_create_handler)

# factory

def factory_project_subparsers(parser: ArgumentParser,
                               interface_subparsers: _SubParsersAction,
                               command_subparsers: _SubParsersAction):

    project_subparser = command_subparsers.add_parser("project")
    project_argparse(project_subparser)

    subcommand_subparsers = project_subparser.add_subparsers(title='subcommand', required=True)

    create_subcommand_subparser = subcommand_subparsers.add_parser("create")
    project_create_argparse(create_subcommand_subparser)