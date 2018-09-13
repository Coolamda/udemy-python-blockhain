def unlimited_arguments(*args, **kwargs):
    for key, value in kwargs.items():
        print(key, value)


unlimited_arguments(1, 2, 3, name="Liam", age=19)
format_list = [1, 2, 3]
print("Stuff: {} {} {}".format(*format_list))


def generate_array(n):
    return list(range(1, n + 1))


def square(x):
    return x * x


def my_map(func, list):
    new_list = []
    for item in list:
        new_list.append(func(item))
    return new_list


def even(number):
    return number % 2 == 0


def my_filter(pred, list):
    new_list = []
    for item in list:
        if (pred(item)):
            new_list.append(item)
    return new_list


def curry_sum(a):
    return lambda b: a + b
