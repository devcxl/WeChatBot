import logging

from config import conf
from typing import List

handlers = [logging.StreamHandler()]

level = logging.INFO


if conf.log.verbose:
    level = logging.DEBUG
    logging.getLogger('itchat').setLevel(logging.INFO)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('openai').setLevel(logging.INFO)

if conf.log.file is not None:
    handlers.append(logging.FileHandler(conf.log.file))

logging.basicConfig(
    level=level,  # 设置日志级别
    format='%(asctime)s - %(name)s [%(levelname)s] %(message)s',
    handlers=handlers
)

log = logging.getLogger('LoadBalancer')


class LoadBalancer:
    def __init__(self, items: List[str]):
        self.items = items
        self.current_index = 0

    def get_next_item(self) -> str:
        if not self.items:
            raise ValueError("No items in the list.")

        next_item = self.items[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.items)
        log.debug(f'current_apikey: {next_item}')
        return next_item
