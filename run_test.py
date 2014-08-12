#!/usr/bin/python

import os
from action_runner import ActionRunner

def main():
    print 'This is example!'
    
    for var in ['TEST_PRE_VAR', 'TEST_VAR', 'TEST_POST_VAR']:
        if os.environ.has_key(var):
            print '[%s] is [%s]' % (var, os.environ[var])
        else:
            print 'No [%s]' % var
        
    runner = ActionRunner()
    runner.do_test_pre().do_test().do_test_post().run()
    
    for var in ['TEST_PRE_VAR', 'TEST_VAR', 'TEST_POST_VAR']:
        if os.environ.has_key(var):
            print '[%s] is [%s]' % (var, os.environ[var])
        else:
            print 'No [%s]' % var
    
if __name__ == '__main__':
    main()
