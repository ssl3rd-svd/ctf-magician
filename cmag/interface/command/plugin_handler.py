from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path

# plugin ... {subcommand}

def plugin_handler(args: Namespace):
    pass

def plugin_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_handler)
    parser.add_argument("-p", "--project", type=Path, default=Path("."))

# plugin ... {subcommand}

def plugin_add_handler(args: Namespace):
    pass

def plugin_add_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_add_handler)
    parser.add_argument("impfrom")
    parser.add_argument("-o", "--options")
    parser.add_argument("--disable", action='store_true')

# plugin ... {subcommand}

def plugin_remove_handler(args: Namespace):
    raise NotImplementedError

def plugin_remove_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_remove_handler)

# plugin ... {subcommand}

def plugin_enable_handler(args: Namespace):
    pass

def plugin_enable_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_enable_handler)
    parser.add_argument("-i", "--id", type=int)
    parser.add_argument("-n", "--callname", type=str)

# plugin ... {subcommand}

def plugin_disable_handler(args: Namespace):
    pass

def plugin_disable_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_disable_handler)
    parser.add_argument("-i", "--id", type=int)
    parser.add_argument("-n", "--callname", type=str)

# plugin ... {subcommand}

def plugin_options_handler(args: Namespace):
    pass

def plugin_options_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_options_handler)
    parser.add_argument("-i", "--id", type=int)
    parser.add_argument("-n", "--callname", type=str)
    parser.add_argument("-o", "--options")

# plugin ... {subcommand}

def plugin_run_handler(args: Namespace):
    pass

def plugin_run_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_run_handler)
    parser.add_argument("-i", "--id", type=int)
    parser.add_argument("-n", "--callname", type=str)
    parser.add_argument("-o", "--options")

# factory

def factory_plugin_subparsers(parser: ArgumentParser,
                              interface_subparsers: _SubParsersAction,
                              command_subparsers: _SubParsersAction):
    
    plugin_subparser = command_subparsers.add_parser("plugin")
    plugin_argparse(plugin_subparser)

    # plugin {subcommand}
    subcommand_subparsers = plugin_subparser.add_subparsers(title="subcommand", required=True)

    # plugin add ...
    plugin_add_subcommand_subparser = subcommand_subparsers.add_parser("add")
    plugin_add_argparse(plugin_add_subcommand_subparser)

    # plugin remove ...
    plugin_remove_subcommand_subparser = subcommand_subparsers.add_parser("remove")
    plugin_remove_argparse(plugin_remove_subcommand_subparser)

    # plugin enable ...
    plugin_enable_subcommand_subparser = subcommand_subparsers.add_parser("enable")
    plugin_enable_argparse(plugin_enable_subcommand_subparser)

    # plugin disable ...
    plugin_disable_subcommand_subparser = subcommand_subparsers.add_parser("disable")
    plugin_disable_argparse(plugin_disable_subcommand_subparser)

    # plugin options ...
    plugin_options_subcommand_subparser = subcommand_subparsers.add_parser("options")
    plugin_options_argparse(plugin_options_subcommand_subparser)

    # plugin run ...
    plugin_run_subcommand_subparser = subcommand_subparsers.add_parser("run")
    plugin_run_argparse(plugin_run_subcommand_subparser)
