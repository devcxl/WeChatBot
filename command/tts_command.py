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
        # 扮演角色
        self.speeker_role = "YoungAdultMale"
        # 可选风格 "narration-relaxed","embarrassed","fearful","cheerful","disgruntled",
        # "serious","angry",sad","depressed","chat",assistant","newscast"
        self.speeker_style = 'cheerful'
        self.speeker_rate = '+5.00%'
        # 风格强度
        self.styledegree = 1.3
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
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts"
            xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="zh-CN">
            <voice name="{self.speeker}"  xml:gender='Female' xml:lang='zh-CN'>
                <s/>
                <mstts:express-as role="{self.speeker_role}" style="{self.speeker_style}" styledegree="{self.styledegree}" >
                    <prosody rate="{self.speeker_rate}">{word}</prosody>
                </mstts:express-as>
                <s/>
            </voice>
        </speak>
        '''
        response = requests.post(
            self.url, headers=self.headers, data=data.encode('utf-8'))
        file = f"{self.VOICE_FILE_PATH}output.mp3"
        if response.status_code == 200:
            with open(file, "wb") as f:
                f.write(response.content)
            return file
        else:
            log.error(f"请求失败，状态码：{response.status_code}")


    # todo
    def pamon_vtis(self, word):
        data = {
            'content': word,
            'speed': '1.1'
        }
        headers = {
            'access-token': 'aeb56737b0984338ad5535de8bc3b8e8'
        }
        resp = requests.get(
            'https://live.ci-s.top/api/paimon', data, headers=headers)
        if resp.status_code == 200:
            with open('pai.wav', 'wb') as f:
                f.write(resp.content)

        resp = requests.get(
            'https://live.ci-s.top/api/paimon/total', headers=headers)
        if resp.status_code == 200:
            print(resp.text)
