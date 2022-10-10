import secrets

from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .models import Register, CostumerOrder
from .forms import CostumerRegisterForm, CostumersLoginForm
import os
import pdfkit
import stripe

publishable_key = 'pk_test_51Lmz12HDCsaazuyLq9utr1EyRHBQamOUryYsJxMpkk6ExrHWva8FnaHiqehjhSw3akLCbXgkBlqs7IjcLoVwnTY500rO0OyLqN'
stripe.api_key =  'sk_test_51Lmz12HDCsaazuyLRrWHvz2MnxC4DKwWzvCW2geOKvzKexkpd6lXnzAh2uqfQMh3cUPMv0IF5C1b29yiXh3FzhFg00zZx524F8'

@app.route('/payment', methods=['POST'])
@login_required
def payment():
	invoice = request.form.get('invoice')
	amount = request.form.get('amount')
	print(amount)
	customer = stripe.Customer.create(
		email=request.form['stripeEmail'],
		source=request.form['stripeToken'])

	charge = stripe.Charge.create(
		customer=customer.id,
		description='MyWifeShop',
		amount=amount,
		currency='czk')

	orders = CostumerOrder.query.filter_by(costumer_id=current_user.id, invoice=invoice).order_by(CostumerOrder.id.desc()).first()
	orders.status = 'Paid'
	db.session.commit()

	return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
	return render_template('costumer/thank.html')


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
		# print(user)
		# print(user.password)
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

# remove un wanted details from shopping cart
def updateshoppingcart():
	for key, product in session['Shoppingcart'].items():
		session.modified = True
		del product['image']
		del product['colors']
	return updateshoppingcart

@app.route('/getorder')
@login_required
def get_order():
	if current_user.is_authenticated:
		costumer_id = current_user.id
		invoice = secrets.token_hex(5)
		updateshoppingcart()
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
			subtotalWithoutTax =("%.2f" % (float(subTotal) - float(tax)))
			grandTotal = ("%.2f" % (float(subTotal)))
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


@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
	if current_user.is_authenticated:
		grandTotal = 0
		subTotal = 0
		costumer_id = current_user.id
		if request.method == 'POST':
			costumer = Register.query.filter_by(id=costumer_id).first()
			orders = CostumerOrder.query.filter_by(costumer_id=costumer_id).order_by(CostumerOrder.id.desc()).first()
			for key, product in orders.orders.items():
				discount = (product['discount']/100) * float(product['price'])
				subTotal = float(product['price']) * int(product['quantity'])
				subTotal -=discount
				tax = "%.2f" % (0.21 * float(subTotal))
				subtotalWithoutTax = float(subTotal) - float(tax)
				grandTotal = float(subTotal)

			# rendered = render_template('costumer/pdf.html',
			#                        invoice=invoice,
			#                        tax=tax,
			#                        subTotal=subTotal,
			#                        subtotalWithoutTax=subtotalWithoutTax,
			#                        grandTotal=grandTotal,
		    #                    costumer=costumer,
		    #                    orders=orders)

			rendered = render_template('costumer/pdf.html', invoice=invoice, tax=tax, grandTotal=grandTotal,
			                           costumer=costumer, orders=orders)
			config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
			pdf = pdfkit.from_string(rendered, False, configuration=config)
			response = make_response(pdf)
			response.headers['content-Type'] = 'application/pdf'
			response.headers['content-Disposition'] = 'atteched; filename=' + invoice + '.pdf'
			return response
	return request(url_for('orders'))

