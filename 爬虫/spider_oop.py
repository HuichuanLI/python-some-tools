from lxml import html
from typing import NamedTuple
import json
import  re
from tqdm import tqdm
from spider_dangdang import spider as dangdang
from spider_jingdong import spider as jd
from spider_yhd import spider as yhd
from spider_tapbao import spider as taobao

import requests


class BootEntity(NamedTuple):
    """ 书本信息 """
    title: str
    price: float
    link: str
    store: str

    def __str__(self):
        return '价格: {self.price} ；名称：{self.title} ; 购买链接：{self.link} 店铺：{self.store}'.format(self=self)



class MySpider(object):

    def __init__(self,sn):
        self.sn = sn

        self.book_list = []

    def jd(self):
        """ 爬取京东的数据 """

        """ 爬取京东的图书数据 """

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        url = 'https://search.jd.com/Search?keyword={0}'.format(self.sn)
        # 获取HTML文档

        resp = requests.get(url, headers=headers)

        resp.encoding = 'utf-8'

        html_doc = resp.text

        # 获取xpath对象
        selector = html.fromstring(html_doc)

        # 找到列表的集合
        ul_list = selector.xpath('//div[@id="J_goodsList"]/ul/li')

        # 解析对应的内容，标题，价格，链接
        for li in tqdm(ul_list):
            # 标题
            title = li.xpath('div/div[@class="p-name"]/a/@title')
            if len(title) == 0:
                continue
            # print(title[0])
            # 购买链接
            link = li.xpath('div/div[@class="p-name"]/a/@href')
            # print(link[0])

            # 价格
            price = li.xpath('div/div[@class="p-price"]/strong/i/text()')
            # print(price[0])

            # 店铺
            store = li.xpath('div//a[@class="curr-shop"]/@title')
            if len(store) == 0:
                continue

            book = BootEntity(
                title=title[0],
                price=price[0].replace('¥', ''),
                link=link[0],
                store=store[0]
            )

            self.book_list.append(book)

        #
        return []

    def taobao(self):
        """ 爬取淘宝的数据 """
        url = 'https://s.taobao.com/search?q={0}'.format(self.sn)
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'cookie': 'cna=RIfSFBumECkCAVoHJVohmNWC; t=afc2b85286206c730343240c7dd1412e; tracknick=%5Cu6B27%5Cu62C9%5Cu5D07%5Cu62DC%5Cu8005; tg=0; enc=xdly13MBq738Xrdc5IcR5GQvDPab7K1bRzjScLpri%2FFn7Ia%2Bl1B8DtBELYjRUTt0kvKiyntdrXCtII6sC80Peg%3D%3D; miid=679180692146832936; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; UM_distinctid=168d7539c13d35-080f783751a89a-133a6850-1aeaa0-168d7539c14e44; _cc_=VFC%2FuZ9ajQ%3D%3D; cookie2=1f3337ad1674250effeebdd345211a63; v=0; _tb_token_=f5eeee3ae7e8b; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=54C8E44C9DDC1623C5C8FAC18A68C30B; l=bBEAgrMHvsOEu_FbBOCiZQ365x7OSIRAguS-Cfyvi_5Iq6L6dmbOl3rwFFp6VA5RscYB4Bayxse9-etXm; isg=BMrKoBpWouP89y75HMf4VZ9lG7bAoltv8IQO1lQDdp2oB2rBPEueJRB1Fyt-98at'
        }

        text = requests.get(url, headers=headers).text

        # 使用正则表达式找到json对象
        p = re.compile(r'g_page_config = (\{.*\});\s*', re.M)

        rest = p.search(text)

        if rest:
            # print(rest.group(1))
            data = json.loads(rest.group(1))
            bk_list = data['mods']['itemlist']['data']['auctions']

            # print(len(bk_list))
            for bk in tqdm(bk_list):
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
                book = BootEntity(
                    title=title,
                    price=price,
                    link=link,
                    store=store
                )
                self.book_list.append(book)
        return []

    def yhd(self):
        """ 爬取一号店的数据 """
        """ 爬取1号店的图书数据 """
        url = 'https://search.yhd.com/c0-0/k{0}/'.format(self.sn)
        # 获取到html源码
        html_doc = requests.get(url).text

        # xpath对象s
        selector = html.fromstring(html_doc)

        # 书籍列表
        ul_list = selector.xpath('//div[@id="itemSearchList"]/div')
        # print(len(ul_list))

        # 解析数据
        for li in tqdm(ul_list):
            # 标题
            title = li.xpath('div/p[@class="proName clearfix"]/a/@title')
            # print(title[0])
            # 价格
            price = li.xpath('div//p[@class="proPrice"]/em/@yhdprice')
            # print(price[0])
            # 购买链接
            link = li.xpath('div/p[@class="proName clearfix"]/a/@href')
            # print(link[0])
            # 店铺
            store = li.xpath('div/p[@class="searh_shop_storeName storeName limit_width"]/a/@title')
            # print(store)
            # print('-----------------------')

            book = BootEntity(
                title=title[0],
                price=price[0],
                link=link[0],
                store=store[0]
            )
            self.book_list.append(book)

        return []

    def dangdang(self):
        url = 'http://search.dangdang.com/?key={sn}&act=input'.format(sn=self.sn)

        # 获取html
        html_data = requests.get(url).text

        selector = html.fromstring(html_data)

        ul_list = selector.xpath('//div[@id="search_nature_rg"]/ul/li')
        for book in tqdm(ul_list):
            title = book.xpath('a/@title')[0]
            # print(title)
            link = book.xpath('a/@href')[0]
            # print(link)
            price = book.xpath('p[@class="price"]/span[@class="search_now_price"]/text()')
            if len(price) == 0:
                price = book.xpath(
                    'div[@class = "ebook_buy"]/p[starts-with(@class,"price")]/span[@class="search_now_price"]/text()')
            price = price[0]

            # print(price.replace("¥", " "))

            store = book.xpath('p[@class="search_shangjia"]/a/text()')
            store = '当当自营' if len(store) == 0 else store[0]
            # print(store)
            # print('-----------------------')

            book = BootEntity(
                title=title,
                price=price.replace("¥", " "),
                link=link,
                store=store
            )

            self.book_list.append(book)
        return  []


    def spider(self):
        """ 得到排序后的数据 """
#        dangdang()
        self.jd()
        print("京东处理完毕")
        self.yhd()
        print("一号店处理完毕")
        self.taobao()
        print("淘宝处理完毕")

        print('数据处理，排序')
        bk_list = sorted(self.book_list, key=lambda item: float(item.price), reverse=False)
        for book in tqdm(bk_list):
            print(book)

if __name__ == '__main__':
    sn = input('请输入东西:')
    MySpider(sn).spider()

