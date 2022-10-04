from argparse import ArgumentParser
from cmag.interface.cui import add_cui_project_args, cui_main

def cli_main(args):
    print("CLI:")
    print(args)
    return 0

def add_cli_project_args(parser, subparsers):
    cli_parser = subparsers.add_parser('cli')
    cli_parser.set_defaults(func=cli_main)
    return cli_parser

def parse_cli_args():
    
    parser = ArgumentParser()
    parser.add_argument("--log-level", default=0)

    subparsers = parser.add_subparsers(dest='interface', required=True)
    cli_parser = add_cli_project_args(parser, subparsers)
    cui_parser = add_cui_project_args(parser, subparsers)

    return parser.parse_args()

def start():
    args = parse_cli_args()
    ec = args.func(args)
    exit(ec)
