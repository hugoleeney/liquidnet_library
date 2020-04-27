from flask import render_template, url_for, flash, redirect

from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = [
    {
        'author': "Corey S",
        "title": "blog post 1",
        "content": "post 1",
        "date_posted": "April 20, 2018"
    },
    {
        'author': "Jane Doe",
        "title": "blog post 2",
        "content": "post 2",
        "date_posted": "April 21, 2018"
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
        except Exception as e:
            print(e)
            flash("User already exists")
            return redirect(url_for('register'))
        db.session.commit()
        flash("Account created for {username}!".format(username=form.username.data), 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title="Register", form=form)


def confirm_user(email, password):
    if email == "asdf@asdf.com" and password == "asdf":
        return True
    else:
        return False

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        if confirm_user(form.email.data, form.password.data):
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check username and password", 'danger')
    return render_template('login.html', title="Register", form=form)

