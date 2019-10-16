import argparse
import sys

from resource_checker.simple_checker.resource_checkers import SessionBasedResourceChecker
from resource_checker.base.exceptions import ResourceCheckerValidationFailure


def main(script_args):
    # TODO: Add packet url processing

    with SessionBasedResourceChecker() as checker:
        try:
            result_url = checker(script_args.url)
            sys.stdout.write(result_url)
        except ResourceCheckerValidationFailure as e:
            sys.stderr.write(str(e))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Check where URL leads after all redirects.',
                                     epilog='Have fun!')
    parser.add_argument('url', type=str, help='URL to check')

    args = parser.parse_args()

    main(args)
