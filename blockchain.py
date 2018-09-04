def create_block(hash, index, transactions):
    return {
        "previous_hash": hash,
        "index": index,
        "transactions": transactions
    }


MINING_REWARD = 10
owner = "Liam"
genesis_block = create_block("", 0, [])
blockchain = [genesis_block]
open_transactions = []
participants = {owner}


def create_transaction(sender, recipient, amount):
    return {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }


def hash_block(block):
    return "-".join([str(block[key]) for key in block])


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(sender, recipient, amount):
    transaction = create_transaction(sender, recipient, amount)
    print(verify_transaction(transaction))
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


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
    reward_transaction = create_transaction("MINING", owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    hashed_block = hash_block(last_block)
    block = create_block(hashed_block, len(blockchain), copied_transactions)
    blockchain.append(block)
    return True


def hack_first_block():
    if len(blockchain) > 0:
        hack_transaction = create_transaction("Marlena", "Liam", 420)
        blockchain[0] = create_block("", 0, [hack_transaction])


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def get_balance(participant):
    tx_sender = [[tx["amount"] for tx in block["transactions"] if tx["sender"] == participant]
                 for block in blockchain]
    open_tx_sender = [tx["amount"]
                      for tx in open_transactions if tx["sender"] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx["amount"] for tx in block["transactions"]
                     if tx["recipient"] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


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
        if add_transaction(owner, recipient, amount):
            print("Added Transaction.")
        else:
            print("Transaction failed.")
    elif choice == "2":
        if mine_block():
            open_transactions = []
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
    print("Marlena:", get_balance("Marlena"))
    print("Liam:", get_balance("Liam"))
else:
    print("User left.")

print("Done!")
