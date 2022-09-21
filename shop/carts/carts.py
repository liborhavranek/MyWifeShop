from flask import render_template, session, request, redirect, url_for, flash, sessions, current_app
from shop import app, db
from shop.products.models import Addproduct
from shop.products.routes import brands, categories


def ManagerDicts(dict1, dict2):
	if isinstance(dict1, list) and isinstance(dict2, list):
		return dict1 + dict2
	elif isinstance(dict1, dict) and isinstance(dict2, dict):
		return dict(list(dict1.items()) + list(dict2.items()))
	return False


@app.route('/addcart', methods=['POST'])
def AddCart():
	try:
		product_id = request.form['product_id']
		quantity = request.form['quantity']
		color = request.form['colors']
		product = Addproduct.query.filter_by(id=product_id).first()
		if product_id and quantity and color and request.method == 'POST':
			DictItem = {product_id:{'name': product.name,
			                        'price': product.price,
			                        'discount': product.discount,
			                        'color': color,
			                        'quantity': quantity,
			                        'image': product.image_1,
			                        'colors': product.colors}}

			if 'Shoppingcart' in session:
				print(session['Shoppingcart'])
				if product_id in session['Shoppingcart']:
					# pokud uživatel klikne 2x na přidat do košíku položka se přidá 2x
					for key, item in session['Shoppingcart'].items():
						if int(key) == int(product_id):
							session.modified = True
							item['quantity'] = int(item["quantity"])
							item['quantity'] += 1

				else:
					session['Shoppingcart'] = ManagerDicts(session['Shoppingcart'], DictItem)
					return redirect(request.referrer)
			else:
				session['Shoppingcart'] = DictItem
				return redirect(request.referrer)
	except Exception as e:
		print(e)
	finally:
		return redirect(request.referrer)


@app.route('/carts')
def getCart():
	if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
		return redirect(url_for('home'))
	subtotal = 0
	grandtotal = 0
	for key, product in session['Shoppingcart'].items():
		discount = (product['discount']/100) * float(product['price'])
		subtotal += float(product['price']) * int(product['quantity'])
		subtotal -= discount
		tax = "%.2f" % (0.21 * float(subtotal))
		subtotal_without_tax = float(subtotal) - float(tax)
		grandtotal = float(subtotal)
	return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, subtotal_without_tax=subtotal_without_tax, brands=brands(), categories=categories())


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
	if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
		return redirect(url_for('home'))
	if request.method == 'POST':
		quantity = request.form.get('quantity')
		color = request.form.get('colors')
		try:
			session.modified = True
			for key, item in session['Shoppingcart'].items():
				if int(key) == code:
					item["quantity"] = quantity
					item["color"] = color
					flash('Item is updatet', 'success')
					return redirect(url_for('getCart'))
		except Exception as e:
			print(e)
			return redirect(url_for('getCart'))


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
	if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
		return redirect(url_for('home'))
	try:
		session.modified = True
		for key, item in session['Shoppingcart'].items():
			if int(key) == id:
				session['Shoppingcart'].pop(key, None)
				flash('Položka byla odstraněna', 'success')
		return redirect(url_for('getCart'))
	except Exception as e:
		print(e)
		return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
	try:
		# Nepoužít session.clear protože by to i odhlásilo uživatele
		# session.clear()
		session.pop('Shoppingcart', None)
		return redirect(url_for('home'))
	except Exception as e:
		print(e)
		return redirect(url_for('home'))


@app.route('/empty')
def empty_cart():
	try:
		session.clear()
		return redirect(url_for('home'))
	except Exception as e:
		print(e)