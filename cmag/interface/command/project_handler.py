from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path

# project ... {subcommand}

def project_handler(args):
    pass

def project_argparse(parser: ArgumentParser):
    parser.set_defaults(func=project_handler)

# project ... create ...

def project_create_handler(args):
    pass

def project_create_argparse(parser: ArgumentParser):
    parser.set_defaults(func=project_create_handler)
    parser.add_argument("path", type=Path)

# factory

def factory_project_subparsers(parser: ArgumentParser,
                               interface_subparsers: _SubParsersAction,
                               command_subparsers: _SubParsersAction):

    project_subparser = command_subparsers.add_parser("project")
    project_argparse(project_subparser)

    subcommand_subparsers = project_subparser.add_subparsers(title='subcommand', required=True)

    create_subcommand_subparser = subcommand_subparsers.add_parser("create")
    project_create_argparse(create_subcommand_subparser)