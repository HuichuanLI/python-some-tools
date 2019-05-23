def foramt_str():

    name = "张三"
    print('欢迎你，%s'% name)
    num = 13.33

    print("您的价格是 %.4f" % num)

    num = 54

    print("您的位置 %d" %num)

    t = (1,2,3,4)
    print("您的数组 %s" % str(t))


    print("{0} ---- {0}".format(t))

    print('宁浩,{username}'.format(username="das"))


if __name__ == '__main__':
    foramt_str()