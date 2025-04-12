from flask import Flask, request, render_template
from main import calculator

app = Flask(__name__)


@app.route("/main_menu", methods=["GET"])
def main_menu():
    pass


@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        data = request.form.get("equation")
        if data and data.strip():
            try:
                result = calculator(data)
                return render_template("calculator_page.html", result=result)
            except ValueError:
                error = "Wrong eqution"
                return render_template("calculator_page.html", error=error)
        else:
            error = "Input equation"
            return render_template("calculator_page.html", error=error)
    else:
        return render_template("calculator_page.html")


if __name__ == "__main__":
    app.run(debug=True)
