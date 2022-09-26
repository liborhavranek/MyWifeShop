import secrets

from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .models import Register, CostumerOrder
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


@app.route('/getorder')
@login_required
def get_order():
	if current_user.is_authenticated:
		costumer_id = current_user.id
		invoice = secrets.token_hex(5)
		try:
			order = CostumerOrder(invoice=invoice, costumer_id=costumer_id, orders=session['Shoppingcart'])
			db.session.add(order)
			db.session.commit()
			session.pop('Shoppingcart')
			flash('Your order has been send successfully', 'success')
			return redirect(url_for('orders', invoice=invoice))
		except Exception as e:
			print(e)
			flash('something went wrong while get order', 'danger')
			return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
	if current_user.is_authenticated:
		grandTotal = 0
		subTotal = 0
		costumer_id = current_user.id
		costumer = Register.query.filter_by(id=costumer_id).first()
		orders = CostumerOrder.query.filter_by(costumer_id=costumer_id).order_by(CostumerOrder.id.desc()).first()
		for key, product in orders.orders.items():
			discount = (product['discount']/100) * float(product['price'])
			subTotal = float(product['price']) * int(product['quantity'])
			subTotal -=discount
			tax = "%.2f" % (0.21 * float(subTotal))
			subtotalWithoutTax = float(subTotal) - float(tax)
			grandTotal = float(subTotal)
	else:
		return redirect(url_for('costumerLogin'))
	return render_template('costumer/order.html',
		                       invoice=invoice,
		                       tax=tax,
		                       subTotal=subTotal,
		                       subtotalWithoutTax=subtotalWithoutTax,
		                       grandTotal=grandTotal,
	                       costumer=costumer,
	                       orders=orders)

