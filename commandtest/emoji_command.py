import logging as log
import requests, json, random, os
from .base_command import BaseCommand


class EmojiCommand(BaseCommand):

    def __init__(self) -> None:
        self.rate = 70
        self.base_path = '/save/'
        self.download_dir = f'{self.base_path}emoji/download/'
        self.upload_dir = f'{self.base_path}emoji/upload/'
        self.bilibili_emoji_path = f'{self.base_path}emoji/bilibili/'
        self.telegram_emoji_path = f'{self.base_path}emoji/telegram/'
        self.api = 'http://www.plapi.tech/api/emoji.php?type=json'
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.bilibili_emoji_path, exist_ok=True)
        os.makedirs(self.telegram_emoji_path, exist_ok=True)

    def getCommandName(self) -> str:
        return '/emoji'

    def execute(self, user=None, params=None, isGroup=False) -> str:
        if len(params) <= 1:
            return self.random_emoji()
        elif len(params) >= 3:
            if params[1] == 'set_rate' and params[2] is not None:
                try:
                    self.rate = int(params[2])
                    return f'使用本地图片的概率：{self.rate}%'
                except (ValueError, TypeError):
                    return 'set_rate failed!'

            if params[1] == 'install' and params[2] == 'bilibili':
                file_names = self.get_visible_files_in_directory(self.bilibili_emoji_path)
                if len(params) >= 4 and params[3] == '-f':
                    self.download_bilibili_emoji()
                    return 'force install bilibili emoji successful!'
                if len(file_names) > 0:
                    return 'installed bilibili emoji'
                else:
                    self.download_bilibili_emoji()
                    return 'install bilibili emoji successful!'

    def random_emoji(self):
        selector = random.randint(0, 100)
        bilibili_emoji = self.get_visible_files_in_directory(self.bilibili_emoji_path)
        telegram_emoji = self.get_visible_files_in_directory(self.telegram_emoji_path)
        total = len(bilibili_emoji) + len(telegram_emoji)
        if selector <= self.rate and total > 0:
            select_emoji = random.randint(0, 1)
            if select_emoji == 1:
                image = self.bilibili_emoji_path + bilibili_emoji[random.randint(0, len(bilibili_emoji) - 1)]
            else:
                image = self.telegram_emoji_path + telegram_emoji[random.randint(0, len(telegram_emoji) - 1)]
            return f'@img@{image}'
        else:
            resp = requests.get(self.api)
            if resp.status_code == 200:
                respBody = json.loads(resp.content);
                emojiResp = requests.get(respBody['text'])
                urlArray = respBody['text'].split('/')
                fileName = urlArray[len(urlArray) - 1]
                if emojiResp.status_code == 200:
                    with open(self.download_dir + fileName, 'wb') as f:
                        f.write(emojiResp.content)
            return f'@img@{self.download_dir + fileName}'

    def download_bilibili_emoji(self):
        # bilibili表情api（免费表情）
        url = 'http://api.bilibili.com/x/emote/user/panel/web?business=reply'
        # 请求头
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52"}
        # 获取json数据
        res = requests.get(url, headers=headers)
        info = res.json()
        # #遍历取出表情url，不需要颜文字
        for package in info['data']['packages'][:3]:
            for emo in package['emote']:
                emo['text'], emo['url']
                jpg = requests.get(emo['url'], headers=headers)
                with open(f'{self.bilibili_emoji_path}{emo["text"]}.gif', 'wb') as file:
                    file.write(jpg.content)

    def get_visible_files_in_directory(self, directory) -> []:
        file_names = []
        for item in os.listdir(directory):
            if not item.startswith('.'):  # 过滤隐藏文件
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    file_names.append(item)
        return file_names
