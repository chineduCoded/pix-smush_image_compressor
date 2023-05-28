#!/.venv/bin/python3
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "PixSmush API"

@app.route("/<name>", methods=["GET"])
def welcome(name):
    return f"Welcome home {name}."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
