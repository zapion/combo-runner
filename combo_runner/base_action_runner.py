import os
import sys
import json
import logging
import subprocess
import action_decorator
from argument_parser import RunTestParser

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BaseActionRunner(object):

    action = action_decorator.action
    parser = RunTestParser()

    def __init__(self):
        # setup logger
        # setup commands lists
        self.pre_commands = []
        self.commands = []
        self.post_commands = []
        # parse the input options
        self.parse_options()

    def parse_options(self):
        self.options, self.tests = self.parser.parse(sys.argv[1:])
        self._load_options()

    def _load_options(self):
        # get --settings option
        self.settings_file = self.options.settings
        self._load_settings_file(self.settings_file)

    def _load_settings_file(self, settings_file=None):
        # Loading settings file
        if settings_file is None:
            logger.info('No settings file, run with default settings.')
            self.settings = {}
        else:
            if not os.path.exists(settings_file):
                logger.warning('No %s file' % (settings_file,))
                self.parser.print_help()
            logger.info('Loading settings from %s' % (settings_file,))
            self.settings = json.load(open(settings_file))

    def _run_command(self, cmd):
        logger.info('Run [%s]\n' % (cmd, ))
        if cmd.startswith('./') and cmd.endswith('.sh'):
            current_process = subprocess.Popen(['bash', '-c', "trap 'echo \"#####__EXIT__#####__EXIT__#####\"; env;' exit; source %s" % cmd],
                                               shell=False, stdout=subprocess.PIPE)
        else:
            current_process = subprocess.Popen(['bash', '-c', "trap 'echo \"#####__EXIT__#####__EXIT__#####\"; env;' exit; %s" % cmd],
                                               shell=False, stdout=subprocess.PIPE)
        is_env_part = False
        env_output_buffer = []
        output_buffer = []
        while True:
            line = current_process.stdout.readline()
            if '#####__EXIT__#####__EXIT__#####' in line:
                is_env_part = True
                continue
            if is_env_part:
                env_output_buffer.append(line)
            else:
                output_buffer.append(line)
                print line,
            if line == '' and current_process.poll() is not None:
                break
        output = ''.join(output_buffer)
        env_vars = ''.join(env_output_buffer)
        return_code = current_process.returncode
        # update os.environ for next commands
        env_vars_list = env_vars.split('\n')
        env_vars_list.remove('')
        os.environ.update(dict([env_var.split('=', 1) for env_var in env_vars_list]))
        return return_code, output, env_vars_list

    def run(self):
        pre_cmd_is_fail = False
        logger.info('Section [PRE-Commands] Start...')
        for cmd in self.pre_commands:
            # run command
            return_code, output, env_vars_list = self._run_command(cmd)
            # if return code is not ZERO, then skip to POST-Commands
            if return_code != 0:
                pre_cmd_is_fail = True
                logger.debug('PRE-Command [%s] return [%d], skip to POST commands.' % (cmd, return_code))
                break
        logger.info('Section [PRE-Commands] End.')

        if not pre_cmd_is_fail:
            logger.info('Section [Commands] Start...')
            for cmd in self.commands:
                # run command
                return_code, output, env_vars_list = self._run_command(cmd)
            logger.info('Section [Commands] End.')

        logger.info('Section [POST-Commands] Start...')
        for cmd in self.post_commands:
            # run command
            return_code, output, env_vars_list = self._run_command(cmd)
        logger.info('Section [POST-Commands] End.')
