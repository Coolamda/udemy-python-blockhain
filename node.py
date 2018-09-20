from flask import Flask
from flask_cors import CORS

from wallet import Wallet

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def get_ui():
    return "App works!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
