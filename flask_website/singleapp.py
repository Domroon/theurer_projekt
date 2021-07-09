from flask import Flask
from flask.templating import render_template
app = Flask(__name__)


buttons = [
    {
        'title': 'Home',
        'link': 'home'
    },
    {
        'title': 'Klavierunterricht',
        'link': 'piano_lesson'
    },
    {
        'title': 'Schlagzeugunterricht',
        'link': 'drums_lesson'
    },
    {
        'title': 'Kontakt',
        'link': 'contact'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", buttons=buttons)


@app.route("/piano_lesson")
def piano_lesson():
    return render_template("piano_lesson.html", title="Klavierunterricht", buttons=buttons)


@app.route("/drums_lesson")
def drums_lesson():
    return render_template("drums_lesson.html", title="Schlagzeugunterricht", buttons=buttons)


@app.route("/contact")
def contact():
    return render_template("contact.html", title="Kontakt", buttons=buttons)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()