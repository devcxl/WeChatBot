import logging
from typing import List

from openai import OpenAI

import config

log = logging.getLogger('LoadBalancer')


class OpenaiLoadBalancer:
    """api_key轮循"""

    def __init__(self, items: List[str]):
        self.items = items
        self.current_index = 0

    def get_next_item(self) -> OpenAI:
        if not self.items:
            raise ValueError("No items in the list.")

        next_item = self.items[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.items)
        log.debug(f'current_apikey: {next_item}')

        return OpenAI(api_key=next_item, base_url=config.api_url)


balancer = OpenaiLoadBalancer(config.api_keys)
