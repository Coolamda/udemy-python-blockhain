from Crypto.PublicKey import RSA
import Crypto.Random
import binascii


class Wallet:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def load_wallet(self):
        pass

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
