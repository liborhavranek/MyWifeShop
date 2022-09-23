from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate
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

#Migrate slouží k rozšíření databáze můžu přidat sloupeček do tabulky nebo ho odebrat
# dokumentace k tomu je tady https://flask-migrate.readthedocs.io/en/latest/
# video je 35 video je v něm i rozšíření tabulkz o sloupeček i smazání sloupečku
migrate = Migrate(app, db)
with app.app_context():
	if db.engine.url.drivername == 'sqlite':
		migrate.init_app(app, db, render_as_batch=True)
	else:
		migrate.init_app(app, db)

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
