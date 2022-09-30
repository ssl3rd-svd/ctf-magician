import parser

def main(args):
    pass

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    exit_code = main(args)
    exit(exit_code)