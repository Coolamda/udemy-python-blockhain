blockchain = []


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction):
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_amount():
    return float(input("Your transaction amount: "))


def get_user_choice():
    return input("Your choice: ")


def print_blockchain_elements():
    for block in blockchain:
        print("Block:", block)
    else:
        print("-" * 20)


def verify_blockchain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid


waiting_for_input = True

while waiting_for_input:
    print("Please choose")
    print("1) Add a new value to blockchain.")
    print("2) Print out blockchain.")
    print("q) Quit program.")
    print("h) Manipulate blockchain.")

    choice = get_user_choice()

    if choice == "1":
        tx_amount = get_transaction_amount()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif choice == "2":
        print_blockchain_elements()
    elif choice == "q":
        waiting_for_input = False
    elif choice == "h":
        blockchain[0] = [2]
    else:
        print("Input is invalid.")
    if not verify_blockchain():
        print("Blockchain is not valid!")
        waiting_for_input = False
else:
    print("User left.")

print("Done!")
