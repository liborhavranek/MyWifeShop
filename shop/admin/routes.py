from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
import os


@app.route('/')
def home():
    return render_template('admin/index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(request.form['password'])
        user_firstname = request.form["firstname"]
        user_lastname = request.form["lastname"]
        user_username = request.form['username']
        user_email = request.form["email"]
        user = User(firstname=user_firstname,
                    lastname=user_lastname,
                    username=user_username,
                    email=user_email,
                    password=hash_password)
        db.session.add(user)
        flash('Thanks for registering', 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registration page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email} You are logedin', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong password try it again','danger')
    return render_template('admin/login.html', form=form, title="Login Page")