def action(func):
    def func_wrapper(self):
        if func.__name__ in self.settings:
            if self.settings[func.__name__]:
                self.logger.debug('The setting [%s] is true.' % func.__name__)
                return func(self, action=True)
            else:
                self.logger.debug('The setting [%s] is false.' % func.__name__)
                return func(self, action=False)
        else:
            self.logger.debug('There is no [%s] in settings file, it will run with default settings.' % func.__name__)
            return func(self, action=True)
    return func_wrapper
