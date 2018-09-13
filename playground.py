def unlimited_arguments(*args, **kwargs):
    for key, value in kwargs.items():
        print(key, value)


unlimited_arguments(1, 2, 3, name="Liam", age=19)
list = [1, 2, 3]
print("Stuff: {} {} {}".format(*list))
