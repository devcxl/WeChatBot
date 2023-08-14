import requests  # 向页面发送请求
from bs4 import BeautifulSoup as BS  # 解析页面
# from .base_command import BaseCommand


class WeiboCommand():
    '''群组'''

    def __init__(self) -> None:
        self.url= 'https://s.weibo.com/top/summary?cate=realtimehot'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
            'Host': 's.weibo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            # 定期更换Cookie
            'Cookie':'SUB=_2AkMThXg5f8NxqwFRmP4UxWrrao11ygDEieKl2YniJRMxHRl-yT9kqmIItRB6OAVW1s1itZ08Sx6SuK7nQxDRMLwNDC8e; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhZSA.MmwAxO86NZGg3NFnv; _s_tentry=passport.weibo.com; Apache=6184921120930.536.1692006159037; SINAGLOBAL=6184921120930.536.1692006159037; ULV=1692006159094:1:1:1:6184921120930.536.1692006159037:'
        }
        self.session = requests.Session()
        self.jar = requests.cookies.RequestsCookieJar()
        # pl_top_realtimehot

        # super().__init__()

    def getCommandName(self):
        return '/weibo'

    def execute(self, user=None, params=None, isGroup=False):
        resp = ''
        r = self.session.get(self.url, headers=self.header)  # 发送请求
        print(r.status_code)
        soup = BS(r.text, 'html.parser')
        div = soup.find('div', id='pl_top_realtimehot')
        table = div.find('table')
        tbody = table.find('tbody')

        trs = tbody.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            for td in tds:
                print(td.text)
        return

        a_tags = table.find_all('a')
        for a in a_tags:
            print(a.text)

        return resp


if __name__ == "__main__":
    weibo =  WeiboCommand()
    weibo.execute()



	