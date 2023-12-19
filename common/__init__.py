import logging

from config import conf

handlers = [logging.StreamHandler()]

level = logging.INFO


if conf.log.verbose:
    level = logging.DEBUG
    logging.getLogger('itchat').setLevel(logging.INFO)

if conf.log.file is not None:
    handlers.append(logging.FileHandler(conf.log.file))

logging.basicConfig(
    level=level,  # 设置日志级别
    format='%(asctime)s - %(name)s [%(levelname)s] %(message)s',
    handlers=handlers
)
