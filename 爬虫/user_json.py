import json


def python_to_json():
    d = {
        'name' : 'python 书',
        'price' : 62.3
    }
    rest = json.dumps(d,indent=4)
    print(rest)

def json_to_python():
    """json 字符串"""
    data = '''
        {
            "name": "Python书籍",
            "origin_price": 66,
            "pub_date": "2018-4-14 17:00:00",
            "store": ["京东", "淘宝"],
            "author": ["张三", "李四", "Jhone"],
            "is_valid": true,
            "is_sale": false,
            "meta": {
                "isbn": "abc-123",
                "pages": 300
            },
            "desc": null
        }
    '''
    rest = json.loads(data)
    print(rest)

def json_to_python_from_file():
    f = open('./static/book.json','r',encoding='utf-8')
    s = f.read()
    print(s)
    res = json.loads(s)
    f.close()
    return

if __name__ == '__main__':
    python_to_json()
    json_to_python()
    json_to_python_from_file()