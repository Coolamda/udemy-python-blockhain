from utility.printable import Printable
from transaction import Transaction


class Block(Printable):
    def __init__(self, previous_hash, index, transactions, proof):
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions
        self.proof = proof

    @staticmethod
    def convert_block(block):
        updated_transactions = [Transaction(
            tx["sender"], tx["recipient"], tx["signature"], tx["amount"]) for tx in block["transactions"]]
        return Block(block["previous_hash"], block["index"], updated_transactions, block["proof"])
