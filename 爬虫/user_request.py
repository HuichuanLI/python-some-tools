import requests


def get_book(sn):
    url = 'http://search.dangdang.com'

    rest = requests.get(url, params={
        'medium': '01',
        'key4': sn,
        'category_path': '01.00.00.00.00.00'
    })

    # rest.encoding = 'utf-8'
    print(rest.text)
    # json

if __name__ == '__main__':
    get_book('9787506380263')
