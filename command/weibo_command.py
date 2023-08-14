import requests  # 向页面发送请求
import random,json,re
from bs4 import BeautifulSoup as BS  # 解析页面
from .base_command import BaseCommand

class WeiboCommand(BaseCommand):
    '''群组'''

    def __init__(self) -> None:

        self.hot_url= 'https://s.weibo.com/top/summary?cate=realtimehot'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
            'Host': 's.weibo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.pattern = r'gen_callback\((.*?)\)'
        self.visitor_url = 'https://passport.weibo.com/visitor/genvisitor'
        self.session = requests.Session()
        t = self.session.post(url=self.visitor_url,data={
            'cb':'gen_callback',
            'fp':'{"os":"3","browser":"Gecko109,0,0,0","fonts":"undefined","screenInfo":"2347*1320*27","plugins":"Portable Document Format::internal-pdf-viewer::PDF Viewer|Portable Document Format::internal-pdf-viewer::Chrome PDF Viewer|Portable Document Format::internal-pdf-viewer::Chromium PDF Viewer|Portable Document Format::internal-pdf-viewer::Microsoft Edge PDF Viewer|Portable Document Format::internal-pdf-viewer::WebKit built-in PDF"}'
        })
        json_str = re.search(self.pattern, t.text).group(1)
        resp = json.loads(json_str)
        tid = resp["data"]["tid"]
        self.cookie_url =f'https://passport.weibo.com/visitor/visitor?a=incarnate&t={tid}&w=2&c=095&gc=&cb=cross_domain&from=weibo&_rand={random.random()}1'
        self.session.cookies.set('tid',f'{tid}__095')
        self.session.get(url=self.cookie_url)
        super().__init__()

    def getCommandName(self):
        return '/weibo'

    def execute(self, user=None, params=None, isGroup=False):
        resp = ''
        r = self.session.get(self.hot_url, headers=self.header)
        soup = BS(r.text, 'html.parser')
        div = soup.find('div', id='pl_top_realtimehot')
        table = div.find('table')
        tbody = table.find('tbody')

        trs = tbody.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            number = tds[0].text
            if number =='•':
                continue
            a =  tds[1].find('a')
            resp += f'{tds[0].text} {a.text}\n'
        return resp


if __name__ == "__main__":
    weibo =  WeiboCommand()
    print(weibo.execute())
    



	