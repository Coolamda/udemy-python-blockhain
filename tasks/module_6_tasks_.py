from datetime import datetime
from random import random, randint


def unique_string():
    return str(randint(1, 10)) + str(datetime.now())


print(unique_string())
