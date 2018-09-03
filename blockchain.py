genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": []
}
blockchain = [genesis_block]
open_transactions = []
owner = "Liam"
participants = {owner}


def hash_block(block):
    return "-".join([str(block[key]) for key in block])


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(sender, recipient, amount):
    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


def get_transaction_value():
    recipient = input("Enter the recipient of the transaction: ")
    amount = float(input("Your transaction amount: "))
    return recipient, amount


def get_user_choice():
    return input("Your choice: ")


def print_blockchain_elements():
    for index, block in enumerate(blockchain):
        print("Block at index " + str(index) + ":", block)
    else:
        print("-" * 20)


def verify_blockchain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        if block["previous_hash"] != hash_block(blockchain[index - 1]):
            return False
    return True


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transactions
    }
    blockchain.append(block)


def hack_first_block():
    if len(blockchain) > 0:
        blockchain[0] = {
            "previous_hash": "",
            "index": 0,
            "transactions": [{
                "sender": "Marlena",
                "recipient": "Liam",
                "amount": 420
            }]
        }


waiting_for_input = True

while waiting_for_input:
    print("Please choose")
    print("1) Add a new value to blockchain.")
    print("2) Mine open transactions.")
    print("3) Print out blockchain.")
    print("4) Print out participants.")
    print("q) Quit program.")
    print("h) Manipulate blockchain.")

    choice = get_user_choice()

    if choice == "1":
        recipient, amount = get_transaction_value()
        add_transaction(owner, recipient, amount)
    elif choice == "2":
        mine_block()
    elif choice == "3":
        print_blockchain_elements()
    elif choice == "4":
        print(participants)
    elif choice == "q":
        waiting_for_input = False
    elif choice == "h":
        hack_first_block()
    else:
        print("Input is invalid.")
    if not verify_blockchain():
        print("Blockchain is not valid!")
        waiting_for_input = False
else:
    print("User left.")

print("Done!")
