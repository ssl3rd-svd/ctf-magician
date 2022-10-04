from cmag.project import CMagProjectManager

def parse_cli_project_args(subparsers):
    pass

def parse_cli_challenge_args(subparsers):
    pass

def parse_cli_file_args(subparsers):
    pass

def parse_cli_url_args(subparsers):
    pass

def parse_cli_socket_args(subparsers):
    pass

def parse_cli_ssh_args(subparsers):
    pass

def parse_cli_args():
    
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", default=0)

    subparsers       = parser.add_subparsers()
    project_parser   = parse_cli_project_args(subparsers)
    challenge_parser = parse_cli_challenge_args(subparsers)
    file_parser      = parse_cli_file_args(subparsers)

def main(args):
    pass

def start():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project-root", required=True)
    parser.add_argument("--modules-path", nargs='*', default=[])
    args = parser.parse_args()
    main(args)
