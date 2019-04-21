import argparse

from git_groomer.cli.parser import _read_config_files


def _parse_args():
    parser = argparse.ArgumentParser(description="Tool to help you take care of your git repo")

    parser.add_argument('command', choices=('blame', 'groom'), help="Command to execute.")
    parser.add_argument('--dry', default=False, required=False, action='store_true',
                        help="Dry run, doesn't actuate upon the repository")
    parser.add_argument('--config_file', required=False, help="Configuration file to use.")
    args = parser.parse_args()
    return args


def get_affected_branches():
    pass


def main():
    args = _parse_args()
    result = _read_config_files(args.config_file)
    print(result)


if __name__ == '__main__':
    main()
