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
        return f'@fil@{self.azure_tts(params[1])}'

    def azure_tts(self, word):
        data = f'''
        <speak version='1.0' xml:lang='zh-CN'>
            <voice xml:lang='zh-CN' xml:gender='Female' name='{self.speeker}'>
                {word}
            </voice>
        </speak>
        '''
        response = requests.post(self.url, headers=self.headers, data=data.encode('utf-8'))
        file = f"{self.VOICE_FILE_PATH}outp.mp3"
        if response.status_code == 200:
            with open(file, "wb") as f:
                f.write(response.content)
            return file
        else:
            log.error(f"请求失败，状态码：{response.status_code}")


if __name__ == "__main__":
    tts = TTSCommand()
    print(tts.execute(params=['/tts', '你可以使用 Python 的 requests 库']))
