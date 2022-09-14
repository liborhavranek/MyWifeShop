from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mywifeshop.db'
app.config['SECRET_KEY'] = 'sKLWkK5eKbkt2qbmJQ59PhISEw7FesBR'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# Nedávat k ostatním importům nahoru, pak to nefunguje a budeš u toho sedět dvě hodiny zase jak debil !!!
from shop.admin import routes
from shop.products import routes
