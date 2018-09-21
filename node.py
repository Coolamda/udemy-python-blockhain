from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route("/", methods=["GET"])
def get_ui():
    return send_from_directory("ui", "node.html")


@app.route("/wallet", methods=["POST"])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance()
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
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    response = {
        "message": "Loading the keys failed."
    }
    return jsonify(response), 500


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
            "block": dict_block,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    response = {
        "message": "Adding a new block failed.",
        "wallet_set_up": wallet.public_key != None
    }
    return jsonify(response), 500


@app.route("/balance", methods=["GET"])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            "message": "Fetched balance successfully.",
            "funds": balance
        }
        return jsonify(response), 200
    response = {
        "message": "Loading balance failed.",
        "wallet_set_up": wallet.public_key != None
    }
    return jsonify(response), 500


@app.route("/transaction", methods=["POST"])
def add_transaction():
    if wallet.public_key == None:
        response = {
            "message": "No wallet set up."
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            "message": "No data found."
        }
        return jsonify(response), 400
    required_fields = ["recipient", "amount"]
    if not all(field in values for field in required_fields):
        response = {
            "message": "Required data is missing."
        }
        return jsonify(response), 400
    recipient = values["recipient"]
    amount = values["amount"]
    signature = wallet.sign_transaction(recipient, amount)
    success = blockchain.add_transaction(
        wallet.public_key, recipient, signature, amount)
    if not success:
        response = {
            "message": "Creating a transactions failed."
        }
        return jsonify(response), 500
    response = {
        "message": "Successfully added transaction.",
        "transaction": {
            "sender": wallet.public_key,
            "recipient": recipient,
            "signature": signature,
            "amount": amount
        },
        "funds": blockchain.get_balance()
    }
    return jsonify(response), 201


@app.route("/transactions", methods=["GET"])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__.copy() for tx in transactions]
    return jsonify(dict_transactions), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
