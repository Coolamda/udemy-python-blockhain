from hashlib import sha256

from utility.hash_util import hash_block


class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict()
                      for tx in transactions]) + last_hash + str(proof)).encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[0:2] == "00"

    @classmethod
    def verify_blockchain(cls, blockchain):
        for index, block in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of Work invalid")
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance = get_balance()
        return sender_balance >= transaction.amount

    @classmethod
    def check_transactions_validity(cls, open_transactions, get_balance):
        return any([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
