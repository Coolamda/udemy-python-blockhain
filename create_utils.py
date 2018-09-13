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
