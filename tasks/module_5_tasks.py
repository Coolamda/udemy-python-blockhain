def exec_func(func, *args):
    for arg in args:
        print("Result: {:^20.2f}".format(func(arg)))


exec_func(lambda arg: arg * 2, 1, 3, 4, 5)
