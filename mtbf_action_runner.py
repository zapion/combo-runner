from base_action_runner import BaseActionRunner


class MTBFActionRunner(BaseActionRunner):

    action = action_decorator.action

    @action
    def mtbf_7mobile_settings(self, action=False):
        if action:
            self.pre_commands.append('./mtbf_7mobile_settings.sh')
        return self

    @action
    def mtbf_change_memory_size(self, action=False):
        if action:
            self.commands.append('./mtbf_change_memory_size.sh')
        return self

    @action
    def mtbf_check_resource(self, action=False):
        if action:
            self.commands.append('./mtbf_check_resource.sh')
        return self

    @action
    def mtbf_environment_cleanup(self, action=False):
        if action:
            self.post_commands.append('./mtbf_environment_cleanup.sh')
        return self

    @action
    def mtbf_memory_nfs(self, action=False):
        if action:
            self.post_commands.append('./mtbf_memory_nfs_indep_symbols.sh')
        return self

    @action
    def mtbf_port_detection(self, action=False):
        if action:
            self.commands.append('./mtbf_port_detection.sh')
        return self

    @action
    def mtbf_prerun(self, action=False):
        if action:
            self.commands.append('./mtbf_prerun.sh')
        return self

    @action
    def mtbf_run_mtbf(self, action=False):
        if action:
            self.commands.append('./mtbf_run_mtbf_multi_new.sh')
        return self

    @action
    def mtbf_shallow_flash(self, action=False):
        if action:
            self.commands.append('./mtbf_shallow_flash_indep_symbols.sh')
        return self

    @action
    def mtbf_virtualenv_setup(self, action=False):
        if action:
            self.commands.append('./mtbf_virtualenv_setup_eggpackage.sh')
        return self
