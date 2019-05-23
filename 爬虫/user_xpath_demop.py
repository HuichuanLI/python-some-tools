from lxml import html


def parse():
    """将html 文件的内容"""
    f = open('./static/index.html', 'r', encoding='utf-8')
    s = f.read()
    selector = html.fromstring(s)

    h3 = selector.xpath('/html/body/h3/text()')
    print(h3[0])
    # // 全部的
    ul = selector.xpath('//ul/li/text()')
    print(ul)
    # for li in ul:
    #     print(li.xpath('text()')[0])

    ul2 = selector.xpath('//ul/li[@class="important"]/text()')
    print(ul2)

    a = selector.xpath('//div[@id ="container"]/a')
    print(a[0].xpath('text()')[0])
    # 标签属性值 href
    print(a[0].xpath('@href')[0])

    p = selector.xpath('/html/body/p[last()]/text()')
    print(p[0])
    f.close()


if __name__ == "__main__":
    parse()
