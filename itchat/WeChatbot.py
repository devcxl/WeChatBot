import logging
import sys

import requests

import itchat
from itchat.utils import test_connect
log = logging.getLogger('WeChatBot')




class WeChatBot:

    def __init__(self, config_path: str, storage_path: str, hot_reload: bool = True):
        if not test_connect():
            log.info("You can't get access to internet or wechatbot domain, so exit.")
            sys.exit()
        self.hot_reload = hot_reload
        self.storage = LocalStorage(directory=storage_path)
        self.session = requests.Session()
        self.alive = False

        if hot_reload:
            info = self.storage.load('wechatbot')
        else:
            # login
            if self.alive:
                log.warning('itchat has already logged in.')
                return
            pass

        itchat.update_friend()

    def login(self, path: str):
        pass

    def push_login(self, r):
        if 'uuid' in r and r.get('ret') in (0, '0'):
            return r['uuid']


    def run(self):
        pass



