from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .models import Register
from .forms import CostumerRegisterForm, CostumersLoginForm
import os


@app.route('/costumer/register', methods=['GET', 'POST'])
def costumer_register():
	form = CostumerRegisterForm()
	if form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(request.form['password'])
		username = request.form["username"]
		email = request.form["email"]
		contact = request.form["contact"]
		first_name = request.form["first_name"]
		last_name = request.form["last_name"]
		state = request.form["state"]
		city = request.form["city"]
		street = request.form["street"]
		zipcode = request.form["zipcode"]
		print()
		register = Register(username=username,
		                    email=email,
		                    contact=contact,
		                    password=hash_password,
		                    first_name=first_name,
		                    last_name=last_name,
		                    state=state,
		                    city=city,
		                    street=street,
		                    zipcode=zipcode)
		db.session.add(register)
		db.session.commit()
		flash(f'Welcome {form.username.data} Thanks you for registering', 'success')
		return redirect(url_for('login'))
	return render_template('costumer/register.html', form=form)


@app.route('/costumer/login', methods=['GET', 'POST'])
def costumerLogin():
	form = CostumersLoginForm()
	if form.validate_on_submit():
		user = Register.query.filter_by(email=request.form["email"]).first()
		print(user)
		print(user.password)
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			flash('You are logt in', 'success')
			next = request.args.get('next')
			return redirect(next or url_for('home'))
		flash('Nesprávné přihlašovací údaje', 'danger')
		return redirect(url_for('costumerLogin'))

	return render_template('costumer/login.html', form=form)


@app.route('/costumer/logout')
def costumer_logout():
	logout_user()
	flash('Uživatel byl úspěšně odhlášen', 'success')
	return redirect(url_for('home'))
