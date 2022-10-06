from argparse import ArgumentParser
from cmag.interface.console import add_console_args

def main(args):
    print(__name__)
    print(args)
    return 0

def parse_cli_args():
    
    parser = ArgumentParser()
    parser.add_argument("--log-level", default=0)

    subparsers = parser.add_subparsers(dest='interface', required=True)
    cui_parser = add_console_args(parser, subparsers)

    return parser.parse_args()

def start():
    args = parse_cli_args()
    ec = args.func(args)
    exit(ec)
