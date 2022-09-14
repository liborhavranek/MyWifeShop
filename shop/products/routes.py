from flask import redirect, render_template, url_for, flash, request
from shop import db, app
from .models import Brand, Category
from .forms import Addproducts
import secrets

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
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
	brands = Brand.query.all()
	categories = Category.query.all()
	form = Addproducts(request.form)
	return render_template('products/addproduct.html', title='Add product page', form=form, brands=brands, categories=categories)