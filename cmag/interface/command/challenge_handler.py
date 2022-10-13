from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path

# challenge ... {subcommand}

def challenge_handler(args):
    pass

def challenge_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_handler)
    parser.add_argument("-p", "--project", type=Path, default=Path("."))

# challenge ... add ...

def challenge_add_handler(args):
    pass

def challenge_add_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_add_handler)
    parser.add_argument("name")

# challenge ... list ...

def challenge_list_handler(args):
    pass

def challenge_list_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_list_handler)
    parser.add_argument("--with-files", action='store_true')

# challenge ... info ...

def challenge_info_handler(args):
    pass

def challenge_info_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_info_handler)
    parser.add_argument("-n", "--name", type=str)
    parser.add_argument("-i", "--id", type=int)

# challenge ... remove ...

def challenge_remove_handler(args):
    pass

def challenge_remove_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_remove_handler)
    parser.add_argument("-n", "--name", type=str)
    parser.add_argument("-i", "--id", type=int)

# challenge ... file ... {subcommand}

def challenge_file_handler(args):
    pass

def challenge_file_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_handler)
    parser.add_argument("challenge", type=int)

# challenge ... file ... create ...

def challenge_file_create_handler(args):
    pass

def challenge_file_create_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_create_handler)
    parser.add_argument("name")

# challenge ... file ... add ...

def challenge_file_add_handler(args):
    pass

def challenge_file_add_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_add_handler)
    parser.add_argument("file", type=Path)
    parser.add_argument("-d", "--dest", type=Path)

# challenge ... file ... list ...

def challenge_file_list_handler(args):
    pass

def challenge_file_list_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_list_handler)

# challenge ... file ... remove ...

def challenge_file_remove_handler(args):
    pass

def challenge_file_remove_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_remove_handler)
    parser.add_argument("-p", "--path", type=Path)
    parser.add_argument("-i", "--id", type=int)

# factory

def factory_challenge_subparsers(parser: ArgumentParser,
                                 interface_subparsers: _SubParsersAction,
                                 command_subparsers: _SubParsersAction):


    challenge_subparser = command_subparsers.add_parser("challenge")
    challenge_argparse(challenge_subparser)

    # challenge {subcommand}
    subcommand_subparsers = challenge_subparser.add_subparsers(title='subcommand', required=True)

    # challenge add ...
    add_subcommand_subparser = subcommand_subparsers.add_parser("add")
    challenge_add_argparse(add_subcommand_subparser)
    
    # challenge list ...
    list_subcommand_subparser = subcommand_subparsers.add_parser("list")
    challenge_list_argparse(list_subcommand_subparser)

    # challenge info ...
    info_subcommand_subparser = subcommand_subparsers.add_parser("info")
    challenge_info_argparse(info_subcommand_subparser)

    # challenge remove ...
    remove_subcommand_subparser = subcommand_subparsers.add_parser("remove")
    challenge_remove_argparse(remove_subcommand_subparser)


    # challenge file ...
    file_subparser = subcommand_subparsers.add_parser("file")
    challenge_file_argparse(file_subparser)

    # challenge file {file_subcommand}
    file_subcommand_subparsers = file_subparser.add_subparsers(title="file_subcommand", required=True)

    # challenge file create ...
    file_create_subcommand_subparser = file_subcommand_subparsers.add_parser("create")
    challenge_file_create_argparse(file_create_subcommand_subparser)

    # challenge file add ...
    file_add_subcommand_subparser = file_subcommand_subparsers.add_parser("add")
    challenge_file_add_argparse(file_add_subcommand_subparser)

    # challenge file path ...
    file_list_subcommand_subparser = file_subcommand_subparsers.add_parser("list")
    challenge_file_list_argparse(file_list_subcommand_subparser)

    # challenge file remove ...
    file_remove_subcommand_subparser = file_subcommand_subparsers.add_parser("remove")
    challenge_file_remove_argparse(file_remove_subcommand_subparser)
