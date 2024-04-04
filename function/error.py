import logging

log = logging.getLogger('function error')


class PluginException(Exception):
    def __init__(self, message="Something went wrong."):
        self.message = message
        super().__init__(self.message)


class PluginUnregisteredException(PluginException):
    def __init__(self, name):
        self.message = f"{name}未注册"
        super().__init__(self.message)


class PlugInExecutionException(PluginException):
    def __init__(self, error):
        self.message = "执行失败"
        super().__init__(self.message)
