import requests
from lxml import html


def spider(sn, book_list=[]):
    """ 爬取1号店的图书数据 """
    url = 'https://search.yhd.com/c0-0/k{0}/'.format(sn)
    # 获取到html源码
    html_doc = requests.get(url).text

    # xpath对象s
    selector = html.fromstring(html_doc)

    # 书籍列表
    ul_list = selector.xpath('//div[@id="itemSearchList"]/div')
    #print(len(ul_list))

    # 解析数据
    for li in ul_list:
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


        book_list.append({
            'title': title[0],
            'price': price[0],
            'link': link[0],
            'store': store[0]
        })



# if __name__ == '__main__':
#     spider('9787115428028')