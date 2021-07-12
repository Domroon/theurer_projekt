from flask import Flask
from flask import request, flash
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ugasgfiiggfgiiasf657sff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    question = db.Column(db.Text, nullable=False)
    date_ask = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Question('{self.email}', '{self.date_ask}')"


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
            flash("Bitte gib eine Email-Adresse ein", 'danger')
        elif not question:
            flash("Bitte gib eine Frage ein", 'danger')
        else:
            question = Question(email=email, question=question)
            db.session.add(question)
            db.session.commit()
            flash("Frage erfolgreich verschickt", 'success')
            #flash(Question.query.all())
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


@app.route("/login", methods=('GET', 'POST'))
def login():
    return render_template("login.html", title="Login", buttons=buttons)


@app.route("/admin", methods=('GET', 'POST'))
def admin():
    return render_template("admin.html", title="Admin", buttons=buttons)


#@app.route("/admin/questions", methods=('GET', 'POST'))
#def admin():
    #return render_template("questions.html", title="Admin", buttons=buttons)



def main():
    try:
        if sys.argv[1] == 'init-db':
            db.drop_all()
            db.create_all()
            print(" * Database initialized")
    except IndexError:
        pass

    app.run(debug=True)


if __name__ == '__main__':
    main()