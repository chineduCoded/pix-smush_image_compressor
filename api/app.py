from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    """Displays home page"""
    return {"message": "This is home"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)