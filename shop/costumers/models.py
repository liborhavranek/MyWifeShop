from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json


@login_manager.user_loader
def user_loader(user_id):
	return Register.query.get(user_id)


class Register(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	# test_name = db.Column(db.String(50), unique=False)
	email = db.Column(db.String(50), unique=True)
	contact = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(200), unique=False)

	first_name = db.Column(db.String(50), unique=False)
	last_name = db.Column(db.String(50), unique=False)

	state = db.Column(db.String(50), unique=False)
	city = db.Column(db.String(50), unique=False)
	street = db.Column(db.String(50), unique=False)
	zipcode = db.Column(db.String(50), unique=False)

	profile = db.Column(db.String(200), unique=False, default='profile.jpg')
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

	def __repr__(self):
		return '<Register %r>' % self.username


class JsonEcodeDict(db.TypeDecorator):
	impl = db.Text

	def process_bind_param(self, value, dialect):
		if value is None:
			return '{}'
		else:
			return json.dumps(value)

	def process_result_value(self, value, dialect):
		if value is None:
			return {}
		else:
			return json.loads(value)


class CostumerOrder(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	invoice = db.Column(db.String(20), unique=True, nullable=False)
	status = db.Column(db.String(20), default='Pending', nullable=False)
	costumer_id = db.Column(db.Integer, unique=False, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	orders = db.Column(JsonEcodeDict, unique=True, nullable=False)

	def __repr__(self):
		return '<CostumerOrder %r>' % self.invoice


db.create_all()
