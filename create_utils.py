from collections import OrderedDict

from block import Block
from transaction import Transaction


def convert_block(block):
    updated_transactions = [Transaction(
        tx["sender"], tx["recipient"], tx["amount"]) for tx in block["transactions"]]
    return Block(block["previous_hash"], block["index"], updated_transactions, block["proof"])
