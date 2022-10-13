from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import List

from argparse import ArgumentParser
from .command import factory_cli_subparsers

def make_argument_parser(subparser_factories: List[function] = []) -> ArgumentParser:
    
    parser = ArgumentParser()

    interface_subparsers = parser.add_subparsers(title='interface', required=True)

    factory_cli_subparsers(parser, interface_subparsers)

    for factory in subparser_factories:
        factory(parser, interface_subparsers)

    return parser