blockchain = []


def get_last_blockchain_value():
    """ Returns the last value of the blockchain. """
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    """ Add new value to blockchain and last element of current blockchain.

    Arguments:
        :transaction_amount: The amount to be added.
        :last_transaction: Last transaction of current blockchain.
    """
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    return float(input("Your transaction amount: "))


tx_amount = get_user_input()
add_value(tx_amount)

tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

print(blockchain)
