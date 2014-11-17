#!/usr/bin/python

import os
from test_action_runner import TestActionRunner


def main():
    print 'This is example!'

    for var in ['TEST_PRE_VAR', 'TEST_VAR', 'TEST_POST_VAR', 'TEAM']:
        if var in os.environ:
            print '[%s] is [%s]' % (var, os.environ[var])
        else:
            print 'No [%s]' % var

    runner = TestActionRunner()
    runner.do_test_pre().do_test().do_test_post()
    runner.run()

    for var in ['TEST_PRE_VAR', 'TEST_VAR', 'TEST_POST_VAR', 'TEAM']:
        if var in os.environ:
            print '[%s] is [%s]' % (var, os.environ[var])
        else:
            print 'No [%s]' % var

if __name__ == '__main__':
    main()
