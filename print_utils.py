def print_balance(user, balance):
    print("Balance of {}: {:6.2f}".format(user, balance))


def print_menu():
    print("Please choose")
    print("1) Add a new value to blockchain.")
    print("2) Mine open transactions.")
    print("3) Print out blockchain.")
    print("4) Check open transactions for validity.")
    print("q) Quit program.")


def print_blockchain_elements(blockchain):
    for index, block in enumerate(blockchain):
        print("Block at index " + str(index) + ":", block)
    else:
        print("-" * 20)
