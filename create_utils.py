from collections import OrderedDict


def create_block(hash, index, transactions, proof):
    return {
        "previous_hash": hash,
        "index": index,
        "transactions": transactions,
        "proof": proof
    }


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
    return create_block(block["previous_hash"],
                        block["index"],
                        updated_transactions,
                        block["proof"])
