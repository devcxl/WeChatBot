import logging

from config import conf


handlers = [logging.StreamHandler()]

level = logging.INFO

if conf.verbose:
    level = logging.DEBUG

if conf.log_file is not None:
    handlers.append(logging.FileHandler(conf.log_file))

logging.basicConfig(
    level=level,  # 设置日志级别
    format='%(asctime)s - %(name)s [%(levelname)s] %(message)s',
    handlers=handlers
)
