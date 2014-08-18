#!/usr/bin/python

import os
from gaiatest_desktopb2g_action_runner import GaiatestDesktopActionRunner


def main():
    runner = GaiatestDesktopActionRunner()
    # parse options
    runner.parse_options()
    # setup the platform and branch
    runner.set_platform(GaiatestDesktopActionRunner.PLATFORM_LINUX_64)
    runner.set_b2g_branch('master', 'master')
    # actions and run
    runner.desktopb2g_download().desktopb2g_run()
    runner.run()

if __name__ == '__main__':
    main()
