from spider_dangdang import spider as dangdang
from spider_jingdong import spider as jd
from spider_yhd import spider as yhd
from spider_tapbao import spider as taobao


def main(sn):
    """ 图书比价工具整合 """
    book_list = []
    # 当当网的数据
    #print('当当网数据爬取完成')
    #dangdang(sn, book_list)

    # 京东网数据
    print('京东网数据爬取完成')
    jd(sn, book_list)

    # 1号店数据
    print('1号店数据爬取完成')
    yhd(sn, book_list)

    # 淘宝
    print('淘宝数据爬取完成')
    taobao(sn, book_list)

    # 打印所有数据列表
    # for book in book_list:
    #     print(book)

    print('----------------开始排序-----------')

    # 排序书的数据
    book_list = sorted(book_list, key=lambda item: float(item["price"]))
    for book in book_list:
        print(book)

if __name__ == '__main__':
    sn = input('请输入ISBN:')
    main(sn)