from .Session import CMagShellSession
from .Shell import CMagShell
from .handlers import *

def add_cui_project_args(parser, subparsers):
    cui_parser = subparsers.add_parser('cui')
    cui_parser.add_argument("project")
    cui_parser.set_defaults(func=cui_main)
    return cui_parser

def cui_main(args):

    from cmag.project import CMagProjectManager

    session = CMagShellSession()
    CMagShell.do_project = CMagCmdProjectHandler(session)
    shell = CMagShell()

    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        shell.do_exit(None)
