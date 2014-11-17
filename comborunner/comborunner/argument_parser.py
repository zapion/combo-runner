import argparse
import sys
import textwrap
from argparse import ArgumentDefaultsHelpFormatter


class RunTestParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Test Runner for Gaiatest/MTBF by TWQA',
            formatter_class=ArgumentDefaultsHelpFormatter,
            epilog=textwrap.dedent('''\
            example:
              $ ./run_test.py
            '''))
        self.parser.add_argument('--settings', help='target build version')

    def parse(self, input):
        return self.parser.parse_args(input)

    def print_help(self):
        return self.parser.print_help()

if __name__ == "__main__":
    parser = RunTestParser()
    if len(sys.argv) > 1:
        print parser.parse(sys.argv[1:])
    else:
        testSample = ["--settings", "gaiatest.json"]
        print parser.parse(testSample)
