from uuid import uuid4

from blockchain import Blockchain
from verification import Verification


class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = "Liam"
        self.blockchain = Blockchain(self.id)

    def get_user_choice(self):
        return input("Your choice: ")

    def print_blockchain_elements(self):
        for index, block in enumerate(self.blockchain.chain):
            print("Block at index " + str(index) + ":", block)
        else:
            print("-" * 20)

    def print_balance(self):
        calculate_balance = self.blockchain.get_balance()
        print("Balance of {}: {:6.2f}".format(self.id, calculate_balance))

    def get_transaction_value(self):
        recipient = input("Enter the recipient of the transaction: ")
        amount = float(input("Your transaction amount: "))
        return recipient, amount

    def listen_for_user_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose")
            print("1) Add a new value to blockchain.")
            print("2) Mine open transactions.")
            print("3) Print out blockchain.")
            print("4) Check open transactions for validity.")
            print("q) Quit program.")
            choice = self.get_user_choice()
            if choice == "1":
                recipient, amount = self.get_transaction_value()
                if self.blockchain.add_transaction(self.id, recipient, amount):
                    print("Added Transaction.")
                else:
                    print("Transaction failed.")
            elif choice == "2":
                if self.blockchain.mine_block():
                    self.blockchain.open_transactions = []
                    self.blockchain.save_data()
                else:
                    print("Block not mined")
            elif choice == "3":
                self.print_blockchain_elements()
            elif choice == "4":
                verifier = Verification()
                print(verifier.check_transactions_validity(
                    self.blockchain.open_transactions, self.blockchain.get_balance))
            elif choice == "q":
                waiting_for_input = False
            else:
                print("Input is invalid.")
            verifier = Verification()
            if not verifier.verify_blockchain(self.blockchain.chain):
                print("Blockchain is not valid!")
                waiting_for_input = False
            self.print_balance()
        else:
            print("User left.")


node = Node()
node.listen_for_user_input()
