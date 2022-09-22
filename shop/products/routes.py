from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos, search
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import os




def brands():
	brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
	return brands


def categories():
	categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
	return categories


# per page znamená počet caret které chci na stránku zorazit
@app.route("/")
def home():
	page = request.args.get('page', 1, type=int)
	products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=5)
	return render_template('products/index.html', products=products, brands=brands(), categories=categories())


@app.route('/product/<int:id>')
def single_page(id):
	product = Addproduct.query.get_or_404(id)
	return render_template('products/single_page.html', product=product, brands=brands(), categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
	page = request.args.get('page', 1, type=int)
	get_b = Brand.query.filter_by(id=id).first_or_404()
	brand = Addproduct.query.filter_by(brand=get_b).paginate(page=page, per_page=5)
	return render_template('products/index.html', brand=brand, brands=brands(), categories=categories(), get_b=get_b)


@app.route('/categories/<int:id>')
def get_category(id):
	page = request.args.get('page', 1, type=int)
	get_cat = Category.query.filter_by(id=id).first_or_404()
	get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=5)
	return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories(), brands=brands(), get_cat=get_cat)

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
		return redirect(url_for('brands'))
	return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods=['POST', 'GET'])
def updatebrand(id):
	if 'email' not in session:
		flash('Prvně se prosím přihlašte', 'danger')
		return redirect(url_for('login'))
	updatebrand = Brand.query.get_or_404(id)
	brand = request.form.get('brand')
	if request.method == "POST":
		updatebrand.name = brand
		flash(f'Brand is updated successfully', 'success')
		db.session.commit()
		return redirect(url_for('brands'))
	return render_template('products/updatebrand.html', title="Update brand page", updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
	brand = Brand.query.get_or_404(id)
	if request.method == 'POST':
		db.session.delete(brand)
		db.session.commit()
		flash(f'The Brand {brand.name} was deleted from the database', 'success')
		return redirect(url_for('admin'))
	flash(f'The brand {brand.name} cant be deleted', 'warning')
	return redirect(url_for('admin'))



@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
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
		return redirect(url_for('admin'))
	return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>', methods=['POST', 'GET'])
def updatecat(id):
	if 'email' not in session:
		flash('Prvně se prosím přihlašte', 'danger')
		return redirect(url_for('login'))
	updatecat = Category.query.get_or_404(id)
	category = request.form.get('category')
	if request.method == "POST":
		updatecat.name = category
		flash(f'Category is updated successfully', 'success')
		db.session.commit()
		return redirect(url_for('categories'))
	return render_template('products/updatebrand.html', title="Update category page", updatecat=updatecat)


@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
	category = Category.query.get_or_404(id)
	if request.method == 'POST':
		db.session.delete(category)
		db.session.commit()
		flash(f'The Brand {category.name} was deleted from the database', 'success')
		return redirect(url_for('admin'))
	flash(f'The brand {category.name} cant be deleted', 'warning')
	return redirect(url_for('admin'))


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


@app.route('/updateproduct/<int:id>', methods=['POST', 'GET'])
def updateproduct(id):
	if 'email' not in session:
		flash('Prvně se prosím přihlašte', 'danger')
		return redirect(url_for('login'))
	brands = Brand.query.all()
	categories = Category.query.all()
	brand = request.form.get('brand')
	category = request.form.get('category')
	product = Addproduct.query.get_or_404(id)
	form = Addproducts(request.form)
	if request.method == "POST":
		product.name = form.name.data
		product.price = form.price.data
		product.discount = form.discount.data
		product.stock = form.stock.data
		product.brand_id = brand
		product.category_id = category
		product.colors = form.colors.data
		product.size = form.size.data
		product.description = form.description.data
		if request.files.get("image_1"):
			try:
				# prvni radek smaze fotku a druhy nahraje novou
				os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
				product.image_1 = photos.save(request.files['image_1'])
			except:
				product.image_1 = photos.save(request.files['image_1'])

		if request.files.get("image_2"):
			try:
				os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
				product.image_2 = photos.save(request.files['image_2'])
			except:
				product.image_2 = photos.save(request.files['image_2'])

		if request.files.get("image_3"):
			try:
				os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
				product.image_3 = photos.save(request.files['image_3'])
			except:
				product.image_3 = photos.save(request.files['image_3'])

		db.session.commit()
		flash(f'Your product has been updated', 'success')
		return redirect('/admin')
	#-------formular bude predvyplneny --------
	form.name.data = product.name
	form.price.data = product.price
	form.discount.data = product.discount
	form.stock.data = product.stock

	form.colors.data = product.colors
	form.size.data = product.size
	form.description.data = product.description
	#/////////////////////////////////
	return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product)


@app.route('/deleteproduct<int:id>', methods=['POST'])
def deleteproduct(id):
	product = Addproduct.query.get_or_404(id)
	if request.method == 'POST':
		try:
			os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
			os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
			os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
		except Exception as e:
			print(e)
		db.session.delete(product)
		db.session.commit()
		flash(f' Produkt {product.name} byl smazán', 'success')
		return redirect(url_for('admin'))
	flash(f'Produkt {product.name} nemůže být smazán')
	return redirect(url_for('admin'))



@app.route('/result')
def result():
	searchword = request.args.get('q')
	products = Addproduct.query.msearch(searchword, fields=['name', 'description'], limit=5)
	return render_template('products/result.html', products=products, brands=brands(), categories=categories())
