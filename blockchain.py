import json
from functools import reduce

from block import Block
from transaction import Transaction
from verification import Verification
from hash_util import hash_block
from create_utils import convert_block
from tx_utils import calc_sum_of_tx
from print_utils import print_balance

MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block("", 0, [], 100)
        self.chain = [genesis_block]
        self.open_transactions = []
        self.hosting_node_id = hosting_node_id
        self.load_data()

    def load_data(self):
        try:
            with open("blockchain.txt", mode="r") as f:
                file_contents = f.readlines()
                json_blockchain = json.loads(file_contents[0][:-1])
                json_open_transaction = json.loads(file_contents[1])
                self.chain = list(map(convert_block, json_blockchain))
                self.open_transactions = [Transaction(
                    tx["sender"], tx["recipient"], tx["amount"]) for tx in json_open_transaction]
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                saveable_blockchain = [block.__dict__ for block in [
                    Block(block_el.previous_hash, block_el.index, [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in self.chain]]
                f.write(json.dumps(saveable_blockchain))
                f.write("\n")
                saveable_transactions = [
                    tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_transactions))
        except IOError:
            print("Saving failed!")

    def proof_of_work(self):
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = 0
        verifier = Verification()
        while not verifier.valid_proof(self.open_transactions, hashed_block, proof):
            proof += 1
        return proof

    def get_last_blockchain_value(self):
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        verifier = Verification()
        if verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            "MINING", self.hosting_node_id, MINING_REWARD)
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(hashed_block, len(self.chain),
                      copied_transactions, proof)
        self.chain.append(block)
        return True

    def get_all_tx_of(self, participant):
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                     for block in self.chain]
        open_tx_sender = [tx.amount
                          for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                        for block in self.chain]
        return tx_sender, tx_recipient

    def get_balance(self):
        tx_sender, tx_recipient = self.get_all_tx_of(self.hosting_node_id)
        amount_sent = reduce(calc_sum_of_tx, tx_sender, 0)
        amount_received = reduce(calc_sum_of_tx, tx_recipient, 0)
        return amount_received - amount_sent
