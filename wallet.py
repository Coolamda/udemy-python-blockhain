from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    def __init__(self, node_id):
        self.public_key = None
        self.private_key = None
        self.node_id = node_id

    def load_wallet(self):
        try:
            with open(f"wallet-{self.node_id}.txt", mode="r") as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
                return True
        except (IOError, IndexError):
            return False

    def save_keys(self):
        if self.public_key is not None and self.private_key is not None:
            try:
                with open(f"wallet-{self.node_id}.txt", mode="w") as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                    return True
            except (IOError, IndexError):
                return False

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def key_to_ascii(self, key):
        return binascii.hexlify(key.exportKey(format="DER")).decode("ascii")

    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return self.key_to_ascii(private_key), self.key_to_ascii(public_key)

    def sign_transaction(self, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(
            binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(self.public_key) + str(recipient) +
                        str(amount)).encode("utf8"))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode("ascii")

    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(((str(transaction.sender) + str(transaction.recipient) +
                         str(transaction.amount)).encode("utf8")))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))
