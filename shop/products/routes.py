from flask import redirect, render_template, url_for, flash, request, session
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
	if 'email' not in session:
		flash('Prvně se prosím přihlašte', 'danger')
		return redirect(url_for('login'))
	if request.method == "POST":
		getbrand = request.form["brand"]
		brand = Brand(name=getbrand)
		db.session.add(brand)
		flash(f'The brand {getbrand} was added to your database', 'success')
		db.session.commit()
		return redirect(url_for('addbrand'))
	return render_template('products/addbrand.html', brands='brands')


@app.route('/addcat', methods=['GET', 'POST'])
def addcategory():
	if 'email' not in session:
		flash('Prvně se prosím přihlašte', 'danger')
		return redirect(url_for('login'))
	if request.method == "POST":
		getcategory = request.form["category"]
		print(getcategory)
		category = Category(name=getcategory)
		db.session.add(category)
		flash(f'The category {getcategory} was added to your database', 'success')
		db.session.commit()
		return redirect(url_for('addbrand'))
	return render_template('products/addbrand.html')

@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
	if 'email' not in session:
		flash('Prvně se prosím přihlašte', 'danger')
		return redirect(url_for('login'))
	brands = Brand.query.all()
	categories = Category.query.all()
	form = Addproducts(request.form)
	if request.method == "POST":
		name = request.form["name"]
		price = request.form["price"]
		discount = request.form["discount"]
		stock = request.form["stock"]
		description = request.form["description"]
		colors = request.form["colors"]
		size = request.form["size"]
		brand = request.form.get('brand')
		print(brand)
		category = request.form.get('category')
		image_1 = photos.save(request.files['image_1'])
		image_2 = photos.save(request.files['image_2'])
		image_3 = photos.save(request.files['image_3'])
		addproduct = Addproduct(name=name,
		                     price=price,
		                     discount=discount,
		                     stock=stock, brand_id=brand, category_id=category,
		                     description=description,
		                     colors=colors,
		                     size=size,
		                     image_1=image_1,
		                     image_2=image_2,
		                     image_3=image_3)
		db.session.add(addproduct)
		flash(f"The product {name} is added to database.", 'success')
		db.session.commit()
		return redirect(url_for('addproduct'))
	return render_template('products/addproduct.html', title='Add product page', form=form, brands=brands, categories=categories)