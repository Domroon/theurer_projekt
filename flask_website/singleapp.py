from flask import Flask
from flask import request, flash
from flask.templating import render_template
app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev')

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


def post_request():
    if request.method == 'POST':
        email = request.form['email']
        question = request.form['question']
        if not email:
            flash("Email required")
        elif not question:
            flash("Question required")
        else:
            flash("Frage erfolgreich verschickt")
            #flash(email)
            #flash(question)


@app.route("/", methods=('GET', 'POST'))
@app.route("/home", methods=('GET', 'POST'))
def home():
    post_request()
    return render_template("home.html", buttons=buttons)


@app.route("/piano_lesson", methods=('GET', 'POST'))
def piano_lesson():
    post_request()
    return render_template("piano_lesson.html", title="Klavierunterricht", buttons=buttons)


@app.route("/drums_lesson", methods=('GET', 'POST'))
def drums_lesson():
    post_request()
    return render_template("drums_lesson.html", title="Schlagzeugunterricht", buttons=buttons)


@app.route("/contact", methods=('GET', 'POST'))
def contact():
    post_request()
    return render_template("contact.html", title="Kontakt", buttons=buttons)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()