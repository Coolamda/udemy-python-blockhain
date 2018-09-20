from utility.printable import Printable
from transaction import Transaction


class Block(Printable):
    def __init__(self, previous_hash, index, transactions, proof):
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions
        self.proof = proof

    def convert_block(self):
        return {
            "previous_hash": self.previous_hash,
            "index": self.index,
            "transactions": [tx.__dict__.copy() for tx in self.transactions],
            "proof": self.proof
        }
