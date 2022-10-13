from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from .utils import open_project

# plugin ... {subcommand}

def plugin_handler(args: Namespace):
    raise NotImplementedError

def plugin_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_handler)


# plugin ... add

def plugin_add_handler(args: Namespace):
    
    if not (project := open_project(args)):
        print("failed.")
        return -1

    plugin = project.plugin_manager.add_plugin(args.impfrom, args.options, not args.disable)
    if not plugin:
        print("failed.")
        return -1

    print("done.")
    return 0

def plugin_add_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_add_handler)
    parser.add_argument("impfrom")
    parser.add_argument("-o", "--options")
    parser.add_argument("--disable", action='store_true')


# plugin ... remove

def plugin_remove_handler(args: Namespace):
    raise NotImplementedError

def plugin_remove_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_remove_handler)


# plugin ... list

def plugin_list_handler(args: Namespace):
    
    from termcolor import colored

    project = open_project(args)
    if not project:
        print("failed.")
        return -1

    print(colored(f"{'id':4} | {'enabled':8} | {'callname':16} | {'impfrom'}", attrs=['bold']))
    for plugin in project.plugin_manager.list_plugins():
        print(f"{str(plugin.id):4} | {str(plugin.enabled).lower():8} | {plugin.callname:16} | {plugin.impfrom}")

def plugin_list_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_list_handler)


# plugin ... enable

def plugin_enable_handler(args: Namespace):

    from cmag.plugin.model import CMagPluginModel

    if not (project := open_project(args)):
        print("failed.")
        return -1

    if not project.plugin_manager.enable_plugin(args.id):
        print("failed.")
        return -1

    print("done.")
    return 0

def plugin_enable_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_enable_handler)
    parser.add_argument("id", type=int)


# plugin ... {subcommand}

def plugin_disable_handler(args: Namespace):

    from cmag.plugin.model import CMagPluginModel

    if not (project := open_project(args)):
        print("failed.")
        return -1

    if not project.plugin_manager.disable_plugin(args.id):
        print("failed.")
        return -1

    print("done.")
    return 0

def plugin_disable_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_disable_handler)
    parser.add_argument("id", type=int)


# plugin ... {subcommand}

def plugin_options_handler(args: Namespace):

    if not (project := open_project(args)):
        print("failed.")
        return -1

    if not args.options:

        options = project.plugin_manager.get_plugin_options(args.id)
        if not options:
            print("failed.")
            return -1

        print(options)
        return 0

    else:

        options = project.plugin_manager.set_plugin_options(args.id, args.options)
        if not options:
            print("failed.")
            return -1

        print("done.")
        return 0

def plugin_options_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_options_handler)
    parser.add_argument("id", type=int)
    parser.add_argument("-o", "--options")


# plugin ... {subcommand}

def plugin_run_handler(args: Namespace):
    
    project = open_project(args)
    if not project:
        print("failed.")
        return -1

    plugin = project.plugin_manager.get_loaded_plugin(args.id)
    if not plugin:
        print("failed.")
        return -1

    if args.options:
        plugin.load_options_from_json(args.options)

    plugin.run()

def plugin_run_argparse(parser: ArgumentParser):
    parser.set_defaults(func=plugin_run_handler)
    parser.add_argument("id", type=int)
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

    # plugin list ...
    plugin_list_subcommand_subparser = subcommand_subparsers.add_parser("list")
    plugin_list_argparse(plugin_list_subcommand_subparser)

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
