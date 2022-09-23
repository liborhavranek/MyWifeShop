from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_msearch import Search
from flask_login import LoginManager
import os

basedir = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mywifeshop.db'
app.config['SECRET_KEY'] = 'sKLWkK5eKbkt2qbmJQ59PhISEw7FesBR'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search =Search()
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'costumerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u'Please login First'

# Nedávat k ostatním importům nahoru, pak to nefunguje a budeš u toho sedět dvě hodiny zase jak debil !!!
from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.costumers import routes
