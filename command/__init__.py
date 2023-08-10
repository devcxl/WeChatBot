from abc import ABC
import logging as log
import requests,json,random,os,itchat

class BaseCommand(ABC):
    def __init__(self) -> None:
        pass

    def getCommandName() -> str:
        raise NotImplementedError

    def execute(self, user=None, params=None, isGroup=False) -> str:
        raise NotImplementedError


class CommandFactory():
    '''命令工厂'''

    def __init__(self) -> None:
        self.commands = {}

    def registerCommand(self, command: BaseCommand) -> None:
        self.commands[command.getCommandName()] = command

    def getCommand(self, commandName) -> BaseCommand:
        command = self.commands.get(commandName)
        if command is None:
            raise ValueError(f"Unknown command: {commandName}")
        return command


class NoticeCommand(BaseCommand):
    '''公告'''

    def __init__(self) -> None:
        super().__init__()

    def getCommandName(self):
        return '/notify'

    def execute(self, user=None, params=None, isGroup=False):
        friends = itchat.get_friends(update=True)
        # friend = itchat.search_friends(name='半颗白菜')[0]
        print(json.dumps(friends, ensure_ascii=False))
        # itchat.send_msg(f"{params[0]}", friend.userName)
        return "/notify command executed."


class GroupCommand(BaseCommand):
    '''群组'''

    def __init__(self) -> None:
        super().__init__()

    def getCommandName(self):
        return '/group'

    def execute(self, user=None, params=None, isGroup=False):
        resp = ''
        chatrooms = itchat.get_chatrooms(True)
        for c in chatrooms:
            resp += f'{c.NickName}\n'
        return resp


class WeatherCommand(BaseCommand):
    '''天气'''

    def __init__(self) -> None:
        self.key = 'b07a3300faadd38f99f1b10b0f9d9a25'
        super().__init__()

    def getCommandName(self):
        return '/weather'

    def execute(self, user=None, params=None, isGroup=False):
        if len(params) <= 1:
            return self.currentWeather(f'{user.province}{user.city}')
        else:
            return self.currentWeather(f'{params[1]}')

    def geoCode(self, address):
        '''根据地址查询出地址的地理信息'''
        AdCodeApi = f'https://restapi.amap.com/v3/geocode/geo?key={self.key}&address={address}'
        res = requests.get(AdCodeApi)
        if res.status_code == 200:
            data = json.loads(res.text)
            return data
        else:
            pass

    def getWeather(self, adcode):
        '''根据城市地区编码查询天气'''
        extensions = 'base'
        weatherApi = f'https://restapi.amap.com/v3/weather/weatherInfo?key={self.key}&city={adcode}&extensions={extensions}'
        res = requests.get(weatherApi)
        if res.status_code == 200:
            data = json.loads(res.text)
            return data
        else:
            pass

    def currentWeather(self, address='北京市'):
        try:
            adcode = self.geoCode(address)['geocodes'][0]['adcode']
            levies = self.getWeather(adcode)['lives'][0]
            reporttime = levies['reporttime']
            province = levies['province']
            city = levies['city']
            weather = levies['weather']
            temperature = levies['temperature']
            winddirection = levies['winddirection']
            windpower = levies['windpower']
            humidity = levies['humidity']
            weatherInfo = f'[{reporttime}]\n{province}{city}\n{weather}{temperature}摄氏度\n{winddirection}风{windpower}级\n空气湿度{humidity}'
            return weatherInfo
        except KeyError:
            return "不支持的地区"


class EmojiCommand(BaseCommand):

    def __init__(self) -> None:
        self.rate = 70
        self.base_path='/tmp/'
        self.download_dir=f'{self.base_path}emoji/download/'
        self.upload_dir=f'{self.base_path}emoji/upload/'
        self.bilibili_emoji_path=f'{self.base_path}emoji/bilibili/'
        self.api = 'http://www.plapi.tech/api/emoji.php?type=json'
        os.makedirs(self.download_dir,exist_ok=True)
        os.makedirs(self.upload_dir,exist_ok=True)
        os.makedirs(self.bilibili_emoji_path,exist_ok=True)

    def getCommandName(self) -> str:
        return '/emoji'

    def execute(self, user=None, params=None, isGroup=False) -> str:
        if len(params)<=1:
            return self.random_emoji() 
        else:
            if params[1] == 'set_rate' and params[2] is not None:
                try:
                    self.rate=int(params[2])
                    return f'使用本地图片的概率：{self.rate}%'
                except (ValueError, TypeError):
                    return 'set_rate failed!'

            if params[1] =='install' and params[2] =='bilibili':
                file_names = self.get_visible_files_in_directory(self.bilibili_emoji_path)
                if len(file_names)>0:
                    return 'installed bilibili emoji'
                else:
                    self.download_bilibili_emoji()
                    return 'install bilibili emoji successful!'
    
    def random_emoji(self):
        selector = random.randint(0,100)
        if selector <= self.rate:
            file_names = self.get_visible_files_in_directory(self.bilibili_emoji_path)
            return f'@img@{self.bilibili_emoji_path + file_names[random.randint(0,len(file_names))]}'
        else:
            resp = requests.get(self.api)
            if resp.status_code == 200:
                respBody = json.loads(resp.content);
                emojiResp = requests.get(respBody['text'])
                urlArray = respBody['text'].split('/')
                fileName = urlArray[len(urlArray)-1]
                if emojiResp.status_code == 200:
                    with open(self.download_dir + fileName,'wb') as f:
                        f.write(emojiResp.content)
            return f'@img@{self.download_dir + fileName}'

    def download_bilibili_emoji(self):
        # bilibili表情api（免费表情）
        url = 'http://api.bilibili.com/x/emote/user/panel/web?business=reply'
        # 请求头
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52"}
        # 获取json数据
        res = requests.get(url, headers=headers)
        info = res.json()
        # #遍历取出表情url，不需要颜文字
        for package in info['data']['packages'][:3]:
            for emo in package['emote']:
                emo['text'], emo['url']
                jpg = requests.get(emo['url'], headers=headers)
                with open(f'{self.bilibili_emoji_path}{emo["text"]}.png', 'wb') as file:
                    file.write(jpg.content)

    def get_visible_files_in_directory(self,directory) -> []:
        file_names = []
        for item in os.listdir(directory):
            if not item.startswith('.'):  # 过滤隐藏文件
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    file_names.append(item)
        return file_names

factory = CommandFactory()
factory.registerCommand(NoticeCommand())
factory.registerCommand(WeatherCommand())
factory.registerCommand(GroupCommand())
factory.registerCommand(EmojiCommand())

# test code
if __name__ == "__main__":
    user = {}
    executor = factory.getCommand('/emoji')
    print(executor.execute(user, ['/emoji','install','bilibili']))
    print(executor.execute(user, ['/emoji','set_rate','30']))
    print(executor.execute(user, ['/emoji','set_rate','A']))
    print(executor.execute(user, ['/emoji']))