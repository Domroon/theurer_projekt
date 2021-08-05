from operator import pos
from werkzeug.utils import redirect
from flask_website.models import Post, User, Question
from flask import request, flash, render_template, url_for
from flask_website import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

buttons = [
    {
        'title': 'Home',
        'link': 'home'
    },
    {
        'title': 'Aktuelles',
        'link': 'news'
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


@app.route("/register", methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        name_exists = User.query.filter_by(name=name).first()
        email_exists = User.query.filter_by(email=email).first()

        if not name_exists and not email_exists:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=name, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Erfolgreich als "{name}" registriert', 'success')
            return redirect(url_for('login'))
        elif name_exists:
            flash(f'Der Name "{name}" ist bereits vergeben', 'danger')
        elif email_exists:
            flash(f'Die Email "{email}" ist bereits vergeben', 'danger')
        
    return render_template("register.html", title="Register", buttons=buttons)


@app.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if User exists
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=request.form.get('rem_checkbox'))
                next_page = request.args.get('next')
                flash("Erfolgreich eingeloggt", 'success')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash("Das Passwort ist falsch", 'danger')
        else:
            flash("Dieser Nutzer existiert nicht", 'danger')

    return render_template("login.html", title="Login", buttons=buttons)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/admin", methods=('GET', 'POST'))
@login_required
def admin():
    return render_template("admin.html", title="Admin", buttons=buttons)


@app.route("/account", methods=('GET', 'POST'))
@login_required
def account():
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        if new_name:
            user = User.query.filter_by(name=new_name).first()
            if user:
                flash("Name bereits vergeben", 'danger')
            else:
                current_user.name = new_name
                db.session.commit()
                flash("Name erfolgreich geändert", 'success')
        if new_email:
            user = User.query.filter_by(email=new_email).first()
            if user:
                flash("Email bereits vergeben", 'danger')
            else:
                current_user.email = new_email
                db.session.commit()
                flash("Email erfolgreich geändert", 'success')
        if new_password:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash("Password erfolgreich geändert", 'success')
    return render_template("account.html", title="Account", buttons=buttons)

@app.route("/news")
def news():
    return render_template("news.html", title="Aktuelles", buttons=buttons)

@app.route("/add_post", methods=('GET', 'POST'))
def add_post():
    if request.method == 'POST':
        post_title = request.form.get('post_title')
        post_text = request.form.get('post_text')
        post = Post(title=post_title, text=post_text)
        db.session.add(post)
        db.session.commit()
    return render_template("add_post.html", title="Hinzufügen", butttons=buttons)

#@app.route("/admin/questions", methods=('GET', 'POST'))
#def admin():
    #return render_template("questions.html", title="Admin", buttons=buttons)
