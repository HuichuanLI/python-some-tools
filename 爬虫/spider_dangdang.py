import requests
from lxml import html


def spider(sn, book_list=[]):
    """dangdang.wang spider"""
    url = 'http://search.dangdang.com/?key={sn}&act=input'.format(sn=sn)

    # 获取html
    html_data = requests.get(url).text

    selector = html.fromstring(html_data)

    ul_list = selector.xpath('//div[@id="search_nature_rg"]/ul/li')
    for book in ul_list:
        title = book.xpath('a/@title')[0]
        #print(title)
        link = book.xpath('a/@href')[0]
        #print(link)
        price = book.xpath('p[@class="price"]/span[@class="search_now_price"]/text()')
        if len(price) == 0:
            price = book.xpath(
                'div[@class = "ebook_buy"]/p[starts-with(@class,"price")]/span[@class="search_now_price"]/text()')
        price = price[0]

        #print(price.replace("¥", " "))

        store = book.xpath('p[@class="search_shangjia"]/a/text()')
        store = '当当自营' if len(store) == 0 else store[0]
        #print(store)
        #print('-----------------------')
        book_list.append({
            'title': title,
            'price': price.replace("¥"," "),
            'link': link,
            'store': store
        })


if __name__ == '__main__':
    sn = '9787111603702'
    spider(sn)
