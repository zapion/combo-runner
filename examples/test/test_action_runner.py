from comborunner import action_decorator
from comborunner.base_action_runner import BaseActionRunner


class TestActionRunner(BaseActionRunner):

    action = action_decorator.action

    @action
    def do_test_pre(self, action=False):
        if action:
            self.pre_commands.append('rm -rf .env; virtualenv .env; source .env/bin/activate; pip install mozdownload')
            self.pre_commands.append('mozdownload -h')
            self.pre_commands.append('export TEAM=MOZTWQA')
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
            self.post_commands.append('mozdownload -h')
            self.post_commands.append('./test_post.sh')
        return self
