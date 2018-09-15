from collections import OrderedDict

from block import Block


def create_transaction(sender, recipient, amount):
    return OrderedDict([
        ("sender", sender),
        ("recipient", recipient),
        ("amount", amount)
    ])


def convert_transaction(tx):
    return create_transaction(tx["sender"], tx["recipient"], tx["amount"])


def convert_block(block):
    updated_transactions = list(
        map(convert_transaction, block["transactions"]))
    return Block(block["previous_hash"], block["index"], updated_transactions, block["proof"])
