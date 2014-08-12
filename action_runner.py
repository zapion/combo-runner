import os
import sys
import json
import logging
import subprocess

from argument_parser import RunTestParser


class ActionRunner(object):

    def __init__(self):
        # setup logger
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.DEBUG)
        # setup commands lists
        self.pre_commands = []
        self.commands = []
        self.post_commands = []
        # parse the input options
        self.parser = RunTestParser()
        self.options = self.parser.parse(sys.argv[1:])
        self._load_options()

    def _load_options(self):
        # get --settings option
        target = self.options.settings
        if target is not None and len(target) > 0:
            self.settings_file = target
        else:
            self.parser.print_help()
            exit(1)
        self._load_settings_file(self.settings_file)

    def _load_settings_file(self, settings_file=None):
        # Loading settings file
        if settings_file is None:
            self.parser.print_help()
        if not os.path.exists(settings_file):
            self.logger.warning('No %s file' % (settings_file,))
            self.parser.print_help()
        self.logger.info('Loading settings from %s' % (settings_file,))
        self.settings = json.load(open(settings_file))

    def action(func):
        def func_wrapper(self):
            if self.settings.has_key(func.__name__):
                if self.settings[func.__name__]:
                    self.logger.debug('The setting [%s] is true.' % func.__name__)
                    return func(self, action=True)
                else:
                    self.logger.debug('The setting [%s] is false.' % func.__name__)
                    return func(self, action=False)
            else:
                self.logger.debug('There is no [%s] in settings file.' % func.__name__)
                return func(self, action=False)
        return func_wrapper

    # TODO: for testing
    @action
    def do_test_pre(self, action=False):
        if action:
            self.pre_commands.append('./test_pre.sh')
        return self

    # TODO: for testing
    @action
    def do_test(self, action=False):
        if action:
            self.commands.append('./test.sh')
        return self

    # TODO: for testing
    @action
    def do_test_post(self, action=False):
        if action:
            self.post_commands.append('./test_post.sh')
        return self

    @action
    def do_7mobile_settings(self, action=False):
        if action:
            self.pre_commands.append('./7mobile_settings.sh')
        return self

    @action
    def change_memory_size(self, action=False):
        if action:
            self.commands.append('./change_memory_size.sh')
        return self

    @action
    def check_resource(self, action=False):
        if action:
            self.commands.append('./check_resource.sh')
        return self

    @action
    def environment_cleanup(self, action=False):
        if action:
            self.post_commands.append('./environment_cleanup.sh')
        return self

    @action
    def memory_nfs(self, action=False):
        if action:
            self.post_commands.append('./memory_nfs_indep_symbols.sh')
        return self

    @action
    def port_detection(self, action=False):
        if action:
            self.commands.append('./port_detection.sh')
        return self

    @action
    def prerun(self, action=False):
        if action:
            self.commands.append('./prerun.sh')
        return self

    @action
    def run_mtbf(self, action=False):
        if action:
            self.commands.append('./run_mtbf_multi_new.sh')
        return self

    @action
    def shallow_flash(self, action=False):
        if action:
            self.commands.append('./shallow_flash_indep_symbols.sh')
        return self

    @action
    def virtualenv_setup(self, action=False):
        if action:
            self.commands.append('./virtualenv_setup_eggpackage.sh')
        return self

    def _run_command(self, cmd):
        self.logger.info('Run [%s]' % (cmd, ))
        #current_process = subprocess.Popen(['bash', '-c', "trap 'env' exit; source \"$1\" > /dev/null 2>&1", '_', cmd],
        current_process = subprocess.Popen(['bash', '-c', "trap 'echo \"#####__EXIT__#####__EXIT__#####\"; env' exit; source \"$1\"", '_', cmd],
                                           shell=False, stdout=subprocess.PIPE)
        output_vars = current_process.communicate()[0]
        output, env_vars = output_vars.split('#####__EXIT__#####__EXIT__#####\n')
        self.logger.info('Output:\n%s' % output)
        return_code = current_process.returncode
        # update os.environ for next commands
        env_vars_list = env_vars.split('\n')
        env_vars_list.remove('')
        os.environ.update(dict([env_var.split('=', 1) for env_var in env_vars_list]))
        return return_code, output, env_vars_list

    def run(self):
        pre_cmd_is_fail = False
        self.logger.info('Section [PRE-Commands] Start...')
        for cmd in self.pre_commands:
            # run command
            return_code, output, env_vars_list = self._run_command(cmd)
            # if return code is not ZERO, then skip to POST-Commands
            if return_code != 0:
                pre_cmd_is_fail = True
                self.logger.debug('PRE-Command [%s] return [%d], skip to POST commands.' % (cmd, return_code))
                break

        if not pre_cmd_is_fail:
            self.logger.info('Section [Commands] Start...')
            for cmd in self.commands:
                # run command
                return_code, output, env_vars_list = self._run_command(cmd)

        self.logger.info('Section [POST-Commands] Start...')
        for cmd in self.post_commands:
            # run command
            return_code, output, env_vars_list = self._run_command(cmd)
