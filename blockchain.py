import json
import requests
from functools import reduce

from block import Block
from transaction import Transaction
from wallet import Wallet
from utility.verification import Verification
from utility.hash_util import hash_block

MINING_REWARD = 10


class Blockchain:
    def __init__(self, public_key, node_id):
        genesis_block = Block("", 0, [], 100)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def save_json_to_chain(self, json_chain):
        updated_blockchain = []
        for block in json_chain:
            converted_tx = [Transaction(
                tx["sender"],
                tx["recipient"],
                tx["signature"],
                tx["amount"]) for tx in block["transactions"]]
            updated_block = Block(
                block["previous_hash"],
                block["index"],
                converted_tx,
                block["proof"])
            updated_blockchain.append(updated_block)
        self.chain = updated_blockchain

    def load_data(self):
        try:
            with open(f"blockchain-{self.node_id}.txt", mode="r") as f:
                file_contents = f.readlines()
                json_blockchain = json.loads(file_contents[0][:-1])
                json_open_transaction = json.loads(file_contents[1][:-1])
                self.save_json_to_chain(json_blockchain)
                self.__open_transactions = [Transaction(
                    tx["sender"],
                    tx["recipient"],
                    tx["signature"],
                    tx["amount"]) for tx in json_open_transaction]
                peer_nodes = json.loads(file_contents[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open(f"blockchain-{self.node_id}.txt", mode="w") as f:
                saveable_blockchain = self.to_serializable_data()
                f.write(json.dumps(saveable_blockchain))
                f.write("\n")
                saveable_transactions = [
                    tx.__dict__.copy() for tx in self.__open_transactions]
                f.write(json.dumps(saveable_transactions))
                f.write("\n")
                f.write(json.dumps(list(self.__peer_nodes)))
        except IOError:
            print("Saving failed!")

    def proof_of_work(self):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions,
                                           hashed_block, proof):
            proof += 1
        return proof

    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, sender, recipient, signature, amount,
                        is_receiving=False):
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            dict_transaction = transaction.__dict__.copy()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = f"http://{node}/broadcast-transaction"
                    try:
                        response = requests.post(url, json=dict_transaction)
                        if (response.status_code == 400 or
                                response.status_code == 500):
                            print("Transaction declined, needs resolving.")
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        if self.public_key is None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            "MINING", self.public_key, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for transaction in copied_transactions:
            if not Wallet.verify_transaction(transaction):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(hashed_block, len(self.__chain),
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            dict_block = block.__dict__.copy()
            dict_block["transactions"] = [
                tx.__dict__ for tx in dict_block["transactions"]]
            url = f"http://{node}/broadcast-block"
            try:
                response = requests.post(url, json={"block": dict_block})
                if response.status_code == 400 or response.status_code == 500:
                    print("Block declined, needs resolving.")
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):
        transactions = [Transaction(
            tx["sender"],
            tx["recipient"],
            tx["signature"],
            tx["amount"]) for tx in block["transactions"]]
        proof_check = Verification.valid_proof(
            transactions[:-1], block["previous_hash"], block["proof"])
        hash_check = hash_block(self.chain[-1]) == block["previous_hash"]
        if not proof_check or not hash_check:
            return False
        converted_block = Block(block["previous_hash"], block["index"],
                                transactions, block["proof"])
        self.__chain.append(converted_block)
        copied_transactions = self.__open_transactions[:]
        for itx in block["transactions"]:
            for opentx in copied_transactions:
                if Verification.compare_dict_tx_and_obj_tx(itx, opentx):
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print("Item was already removed")
        self.save_data()
        return True

    def get_all_tx_of(self, participant):
        tx_sender = [[tx.amount
                      for tx
                      in block.transactions
                      if tx.sender == participant]
                     for block in self.__chain]
        open_tx_sender = [tx.amount
                          for tx
                          in self.__open_transactions
                          if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        tx_recipient = [[tx.amount
                         for tx
                         in block.transactions
                         if tx.recipient == participant]
                        for block in self.__chain]
        return tx_sender, tx_recipient

    def get_balance(self, sender=None):
        if sender is None:
            if self.public_key is None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender, tx_recipient = self.get_all_tx_of(participant)
        amount_sent = reduce(self.calc_sum_of_tx, tx_sender, 0)
        amount_received = reduce(self.calc_sum_of_tx, tx_recipient, 0)
        return amount_received - amount_sent

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = f"http://{node}/chain"
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(
                    block["previous_hash"],
                    block["index"],
                    block["transactions"],
                    block["proof"]) for block in node_chain]
                for block in node_chain:
                    updated_transaction = [Transaction(
                        tx["sender"],
                        tx["recipient"],
                        tx["signature"],
                        tx["amount"]) for tx in block.transactions]
                    block.transactions = updated_transaction
                node_chain_length = len(node_chain)
                local_chain_length = len(self.chain)
                if (node_chain_length > local_chain_length and
                        Verification.verify_blockchain(node_chain)):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
            self.resolve_conflicts = False
            self.chain = winner_chain
            if replace:
                self.__open_transactions == []
            self.save_data()
            return replace

    def calc_sum_of_tx(self, tx_sum, tx_amount):
        if tx_amount:
            return tx_sum + sum(tx_amount)
        return tx_sum

    def to_serializable_data(self):
        return [block.__dict__
                for block
                in [Block(
                    block_el.previous_hash,
                    block_el.index,
                    [tx.__dict__ for tx in block_el.transactions],
                    block_el.proof)
                    for block_el
                    in self.__chain]]

    def add_peer_node(self, node):
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)
