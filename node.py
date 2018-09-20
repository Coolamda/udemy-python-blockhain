from flask import Flask, jsonify
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route("/wallet", methods=["POST"])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key
        }
        return jsonify(response), 201
    response = {
        "message": "Saving the keys failed."
    }
    return jsonify(response), 500


@app.route("/wallet", methods=["GET"])
def load_keys():
    if wallet.load_wallet():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key
        }
        return jsonify(response), 201
    response = {
        "message": "Loading the keys failed."
    }
    return jsonify(response), 500


@app.route("/", methods=["GET"])
def get_ui():
    return "App works!"


@app.route("/chain", methods=["GET"])
def get_chain():
    serializable_chain = blockchain.convert_blocks_to_serializable_data()
    return jsonify(serializable_chain), 200


@app.route("/mine", methods=["POST"])
def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.convert_block()
        response = {
            "message": "Block added successfuly",
            "block": dict_block
        }
        return jsonify(response), 201
    response = {
        "message": "Adding a new block failed."
    }
    return jsonify(response), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
