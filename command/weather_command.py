import requests,json

from .base_command import BaseCommand

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

