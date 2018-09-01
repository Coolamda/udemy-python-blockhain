names = ["Liam", "Marlena", "Colin", "Johannes"]


def has_n(string):
    """ Takes a string and returns True if it contains
    'n' or 'N'
    """
    return "n" in string.lower()


for name in names:
    if len(name) > 5 and has_n(name):
        print(len(name))

while len(names) > 0:
    names.pop()

print(names)
