import os
from comborunner import action_decorator
from comborunner.base_action_runner import BaseActionRunner


class GaiatestDesktopActionRunner(BaseActionRunner):

    action = action_decorator.action

    PLATFORM_LINUX_64 = 'linux64'
    PLATFORM_LINUX_32 = 'linux32'
    PLATFORM_MACOSX = 'mac'

    def __init__(self):
        os.environ['DESKTOPB2G_OS_PLATFORM'] = self.PLATFORM_LINUX_64
        os.environ['DESKTOPB2G_BRANCH'] = 'master'
        os.environ['GAIA_BRANCH'] = 'master'
        group = self.parser.parser.add_argument_group('Gaiatest of Desktop B2G')
        group.add_argument('--testvars', required=True, help='path to a json file with any test data required')
        group.add_argument('--desktopb2g_dir', help='path to a desktop B2G folder, skip download action and run with existing desktop B2G')
        group.add_argument('--type', default='b2g', help='the type of test to run')
        #group.add_argument('--tests', default='gaiatest/tests/functional/manifest.ini', help='test file, dir or manifest.')
        group.add_argument('--tests', default='gaia/tests/python/gaia-ui-tests/gaiatest/tests/functional/manifest.ini',
                           help='test file, dir or manifest.')
        super(GaiatestDesktopActionRunner, self).__init__()

    def parse_options(self):
        super(GaiatestDesktopActionRunner, self).parse_options()

        self.testvars_file = self.options.testvars
        if not os.path.isfile(self.testvars_file):
            self.logger.error('No testvars file [%s].' % self.testvars_file)
            exit(1)
        else:
            self.logger.info('Set env[B2G_GAIATEST_TESTVARS] to [%s].' % self.testvars_file)
            os.environ['B2G_GAIATEST_TESTVARS'] = self.testvars_file

        self.desktopb2g_dir = self.options.desktopb2g_dir
        if self.desktopb2g_dir is None:
            pass
        elif not os.path.isdir(self.desktopb2g_dir):
            self.logger.error('No desktopb2g folder [%s].' % self.desktopb2g_dir)
            exit(1)
        else:
            if 'desktopb2g_download' in self.settings:
                self.logger.info('There is [%s] setting, which value is [%s], in settings file.' % ('desktopb2g_download', self.settings['desktopb2g_download']))
            else:
                # skip download action
                self.logger.info('There is no [%s] setting in settings file.' % 'desktopb2g_download')
                self.logger.info('Set [%s] setting to [False].' % 'desktopb2g_download')
                self.settings['desktopb2g_download'] = False
                # set desktop b2g folder
                self.logger.info('Set env[DESKTOPB2G_DIR] to [%s].' % self.desktopb2g_dir)
                os.environ['DESKTOPB2G_DIR'] = self.desktopb2g_dir

        self.type = self.options.type
        os.environ['B2G_GAIATEST_TYPE'] = self.type
        self.tests = os.path.abspath(self.options.tests)
        if not os.path.isfile(self.tests) and not os.path.isdir(self.tests):
            self.logger.error('must specify one or more test files, manifests, or directories')
            exit(1)
        os.environ['B2G_GAIATEST_TESTS'] = self.tests

    def set_platform(self, platform=PLATFORM_LINUX_64):
        self.logger.info('Set env[DESKTOPB2G_OS_PLATFORM] to [%s].' % platform)
        os.environ['DESKTOPB2G_OS_PLATFORM'] = platform

    def set_b2g_branch(self, desktopb2g_branch='master', gaia_branch='master'):
        self.logger.info('Set env[DESKTOPB2G_BRANCH] to [%s].' % desktopb2g_branch)
        self.logger.info('Set env[GAIA_BRANCH] to [%s].' % gaia_branch)
        os.environ['DESKTOPB2G_BRANCH'] = desktopb2g_branch
        os.environ['GAIA_BRANCH'] = gaia_branch

    @action(enabled=False)
    def desktopb2g_download(self):
        self.pre_commands.append('./gaiatest_desktopb2g_download.sh')
        return self

    @action(enabled=False)
    def desktopb2g_run(self):
        if enabled:
            self.commands.append('./gaiatest_desktopb2g_run.sh')
        return self
