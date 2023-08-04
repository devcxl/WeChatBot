class BaseCommand():
    def __init__(self) -> None:
        pass

    def getCommand() -> str:
        raise NotImplementedError

    def execute(self, user=None, params=None) -> str:
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

    def execute(self, user=None, params=None):
        import itchat
        import json
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

    def execute(self, user=None, params=None):
        import itchat
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

    def execute(self, user=None, params=None):
        if params[1] is None:
            return self.currentWeather(f'{user.province}{user.city}')
        else:
            return self.currentWeather(f'{params[1]}')

    def geoCode(self, address):
        import requests
        import json
        '''根据地址查询出地址的地理信息'''
        AdCodeApi = f'https://restapi.amap.com/v3/geocode/geo?key={self.key}&address={address}'
        res = requests.get(AdCodeApi)
        if res.status_code == 200:
            data = json.loads(res.text)
            return data
        else:
            pass

    def getWeather(self, adcode):
        import requests
        import json
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


factory = CommandFactory()
factory.registerCommand(NoticeCommand())
factory.registerCommand(WeatherCommand())
factory.registerCommand(GroupCommand())
