from functools import reduce
from hashlib import sha256
import json


def create_block(hash, index, transactions, proof):
    return {
        "previous_hash": hash,
        "index": index,
        "transactions": transactions,
        "proof": proof
    }


MINING_REWARD = 10
owner = "Liam"
genesis_block = create_block("", 0, [], 100)
blockchain = [genesis_block]
open_transactions = []
participants = {owner}


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + last_hash + str(proof)).encode()
    guess_hash = sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == "00"


def create_transaction(sender, recipient, amount):
    return {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }


def hash_block(block):
    return sha256(json.dumps(block).encode()).hexdigest()


def proof_of_work():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, hashed_block, proof):
        proof += 1
    return proof


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(sender, recipient, amount):
    transaction = create_transaction(sender, recipient, amount)
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
        if not valid_proof(block["transactions"][:-1], block["previous_hash"], block["proof"]):
            print("Proof of Work invalid")
            return False
    return True


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = create_transaction("MINING", owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = create_block(hashed_block, len(blockchain),
                         copied_transactions, proof)
    blockchain.append(block)
    return True


def hack_first_block():
    if len(blockchain) > 0:
        hacked_transaction = create_transaction("Marlena", "Liam", 420)
        blockchain[0] = create_block("", 0, [hacked_transaction], 100)


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def calc_sum_of_tx(tx_sum, tx_amount):
    if tx_amount:
        return tx_sum + sum(tx_amount)
    return tx_sum


def all_tx_in_blockchain_of(participant, kind):
    return [[tx["amount"] for tx in block["transactions"] if tx[kind] == participant]
            for block in blockchain]


def get_all_tx_of(participant):
    tx_sender = all_tx_in_blockchain_of(participant, "sender")
    open_tx_sender = [tx["amount"]
                      for tx in open_transactions if tx["sender"] == participant]
    tx_sender.append(open_tx_sender)
    tx_recipient = all_tx_in_blockchain_of(participant, "recipient")
    return tx_sender, tx_recipient


def get_balance(participant):
    tx_sender, tx_recipient = get_all_tx_of(participant)
    amount_sent = reduce(calc_sum_of_tx, tx_sender, 0)
    amount_received = reduce(calc_sum_of_tx, tx_recipient, 0)
    return amount_received - amount_sent


def check_transactions_validity():
    return any([verify_transaction(tx) for tx in open_transactions])


def print_balance(user):
    print("Balance of {}: {:6.2f}".format(user, get_balance(user)))


waiting_for_input = True

while waiting_for_input:
    print("Please choose")
    print("1) Add a new value to blockchain.")
    print("2) Mine open transactions.")
    print("3) Print out blockchain.")
    print("4) Print out participants.")
    print("5) Check open transactions for validity.")
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
    elif choice == "5":
        print(check_transactions_validity())
    elif choice == "q":
        waiting_for_input = False
    elif choice == "h":
        hack_first_block()
    else:
        print("Input is invalid.")
    if not verify_blockchain():
        print("Blockchain is not valid!")
        waiting_for_input = False
    print_balance("Marlena")
    print_balance("Liam")
else:
    print("User left.")

print("Done!")
