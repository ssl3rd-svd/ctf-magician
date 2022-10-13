from argparse import ArgumentParser
from cmag.interface.arguments import make_argument_parser

def start():
    parser: ArgumentParser = make_argument_parser()
    print(parser.parse_args())