from flask import render_template, session, request, redirect, url_for, flash, sessions, current_app
from shop import app, db
from shop.products.models import Addproduct


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
		colors = request.form['colors']
		product = Addproduct.query.filter_by(id=product_id).first()
		if product_id and quantity and colors and request.method == 'POST':
			DictItem = {product_id:{'name': product.name,
			                        'price': product.price,
			                        'discount': product.discount,
			                        'colors': colors,
			                        'quantity': quantity,
			                        'image': product.image_1}}

			if 'Shoppingcart' in session:
				print(session['Shoppingcart'])
				if product_id in session['Shoppingcart']:
					print("This product is alredy in cart")
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