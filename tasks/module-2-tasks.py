name = input("What is your name?\n")
age = int(input("And how old are you?\n"))


def printName():
    """ Print name and age to the console. """
    print("Hello, I am " + name + " and " + str(age) + " years old!")


def withAnd(string_one, string_two):
    """ Take 2 strings and return them with an '&' inbetween.
    Arguments:
        :string_one: First string
        :string_two: Second string
    """
    print(string_one + " & " + string_two)


def calcDecades():
    """ Calculate the decades I already lived. """
    return age // 10


print(calcDecades())
