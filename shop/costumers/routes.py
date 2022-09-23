from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos, search, bcrypt
from .models import Register
from .forms import CostumerRegisterForm
import os


@app.route('/costumer/register', methods=['GET', 'POST'])
def costumer_register():
	form = CostumerRegisterForm(request.form)
	if request.method == 'POST':
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