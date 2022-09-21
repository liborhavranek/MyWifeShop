from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from shop.products.models import Addproduct, Brand, Category
from .models import User


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Prvně se prosím přihlašte', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)


@app.route('/brands')
def brands():
    if 'email' not in session:
        flash('Prvně se prosím přihlašte', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brand Page', brands=brands)


@app.route('/category')
def categories():
    if 'email' not in session:
        flash('Prvně se prosím přihlašte', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Category Page', categories=categories)


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
        db.session.commit()
        flash('Thanks for registering', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form, title="Registration page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=request.form["email"]).first()
        print(user)
        print(user.password)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {request.form["email"]} You are logedin', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong password try it again', 'danger')
    return render_template('admin/login.html', form=form, title="Login Page")
