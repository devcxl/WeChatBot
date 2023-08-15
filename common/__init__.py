import logging


class Struct(object):
    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value


class Logger:
    def __init__(self, name, log_file=None, level=logging.INFO) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handlers = [logging.StreamHandler()]
        if log_file is not None:
            self.handlers.append(logging.FileHandler(log_file))
        # 配置日志基本设置
        logging.basicConfig(
            level=level,  # 设置日志级别
            format='%(asctime)s - %(name)s [%(levelname)s] %(message)s',
            handlers=self.handlers
        )

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
