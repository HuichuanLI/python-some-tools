import requests
from lxml import html
import json

import re


def spider(sn, book_list=[]):
    url = 'https://s.taobao.com/search?q={0}'.format(sn)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'cookie': 'cna=RIfSFBumECkCAVoHJVohmNWC; t=afc2b85286206c730343240c7dd1412e; tracknick=%5Cu6B27%5Cu62C9%5Cu5D07%5Cu62DC%5Cu8005; tg=0; enc=xdly13MBq738Xrdc5IcR5GQvDPab7K1bRzjScLpri%2FFn7Ia%2Bl1B8DtBELYjRUTt0kvKiyntdrXCtII6sC80Peg%3D%3D; miid=679180692146832936; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; UM_distinctid=168d7539c13d35-080f783751a89a-133a6850-1aeaa0-168d7539c14e44; _cc_=VFC%2FuZ9ajQ%3D%3D; cookie2=1f3337ad1674250effeebdd345211a63; v=0; _tb_token_=f5eeee3ae7e8b; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=54C8E44C9DDC1623C5C8FAC18A68C30B; l=bBEAgrMHvsOEu_FbBOCiZQ365x7OSIRAguS-Cfyvi_5Iq6L6dmbOl3rwFFp6VA5RscYB4Bayxse9-etXm; isg=BMrKoBpWouP89y75HMf4VZ9lG7bAoltv8IQO1lQDdp2oB2rBPEueJRB1Fyt-98at'
    }

    text = requests.get(url, headers=headers).text

    # 使用正则表达式找到json对象
    p = re.compile(r'g_page_config = (\{.*\});\s*', re.M)

    rest = p.search(text)

    if rest:
        #print(rest.group(1))
        data = json.loads(rest.group(1))
        bk_list = data['mods']['itemlist']['data']['auctions']

        #print(len(bk_list))
        for bk in bk_list:
            # 标题
            title = bk["raw_title"]
            # print(title)
            # 价格
            price = bk["view_price"]
            # print(price)
            # 购买链接
            link = bk["detail_url"]
            # print(link)
            # 商家
            store = bk["nick"]
            # print(store)
            book_list.append({'title': title, 'price': price, 'link': link, 'store': store})
            # print('{title}:{price}:{link}:{store}'.format(title=title, price=price, link=link, store=store))
            # print('-----------------------')

if __name__ == '__main__':
    spider('9787115428028')
