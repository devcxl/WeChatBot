from .base_command import BaseCommand
import os
import requests
import logging as log


class TTSCommand(BaseCommand):
    '''群组'''

    def __init__(self) -> None:
        self.speech_key = "315920d2221047a490a5c1cb32e531ed"
        self.service_region = "eastasia"
        self.speeker = "zh-CN-XiaoxiaoNeural"
        self.url = f"https://{self.service_region}.tts.speech.microsoft.com/cognitiveservices/v1"
        self.headers = {
            "Ocp-Apim-Subscription-Key": f"{self.speech_key}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "ChatBot"
        }
        self.VOICE_FILE_PATH = '/save/tts/'
        os.makedirs(self.VOICE_FILE_PATH, exist_ok=True)
        super().__init__()

    def getCommandName(self):
        return '/tts'

    def execute(self, user=None, params=None, isGroup=False):
        return f'@fil@{self.azure_tts(params[1:])}'

    def azure_tts(self, word):
        data = f'''
        <speak version='1.0' xml:lang='zh-CN'>
            <voice xml:lang='zh-CN' xml:gender='Female' name='{self.speeker}'>
                {word}
            </voice>
        </speak>
        '''
        response = requests.post(self.url, headers=self.headers, data=data.encode('utf-8'))
        file = f"{self.VOICE_FILE_PATH}output.mp3"
        if response.status_code == 200:
            with open(file, "wb") as f:
                f.write(response.content)
            return file
        else:
            log.error(f"请求失败，状态码：{response.status_code}")


if __name__ == "__main__":
    tts = TTSCommand()
    print(tts.execute(params=['/tts', '你可以使用 Python 的 requests 库']))
    # curl -X 'GET' \
    #   'http://127.0.0.1/api/paimon?content=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E6%88%91%E6%98%AF%E6%B4%BE%E8%92%99%E3%80%82&speed=1' \
    #   -H 'accept: application/json' \
    #   -H 'access-token: f4eaace55d3240e2b81e235c300f4a9d'
    import requests

    data = {
        'content':'数字生命计划越来越接近于落地。哈哈哈',
        'speed':'1.1'
    }
    headers = {
        'access-token':'aeb56737b0984338ad5535de8bc3b8e8'
    }
    resp = requests.get('https://live.ci-s.top/api/paimon',data,headers=headers)
    if resp.status_code ==200:
        with open('pai.wav','wb') as f:
            f.write(resp.content)

    resp = requests.get('https://live.ci-s.top/api/paimon/total',headers=headers)
    if resp.status_code ==200:
        print(resp.text)