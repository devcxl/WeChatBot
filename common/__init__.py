import logging
import os
from logging.handlers import TimedRotatingFileHandler

import config

handlers = [logging.StreamHandler()]

level = logging.INFO

if config.debug:
    level = logging.DEBUG

logging.getLogger('itchat').setLevel(level)
logging.getLogger('httpx').setLevel(logging.INFO)
# 设置文件日志 每天分割 备份七天
handler = TimedRotatingFileHandler(os.path.join(config.data_dirs, 'bot.log'), when='midnight', interval=1,
                                   backupCount=7)
handler.suffix = "%Y%m%d"
handlers.append(handler)

logging.basicConfig(
    level=level,  # 设置日志级别
    format='%(asctime)s - %(name)s [%(levelname)s] %(message)s',
    handlers=handlers
)
