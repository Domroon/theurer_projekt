from flask import Flask
from flask.templating import render_template
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()