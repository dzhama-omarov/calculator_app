from flask import Flask

app = Flask(__name__)


@app.route("main_menu", methods=["GET"])
def main_menu():
    pass


if __name__ == "__main__":
    app.run(debug=True)
