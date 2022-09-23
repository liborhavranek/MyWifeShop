from wtforms import Form, StringField,TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register

class CostumerRegisterForm(FlaskForm):
	username = StringField('Username: ', [validators.DataRequired()])
	email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
	contact = StringField('Telefon: ', [validators.DataRequired()])
	password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match')])
	confirm = PasswordField('Repeat password: ', [validators.DataRequired()])

	first_name = StringField('Jmeno: ', [validators.DataRequired()])
	last_name = StringField('Prijmeni: ', [validators.DataRequired()])

	state = StringField('Zeme: ', [validators.DataRequired()])
	city = StringField('Mesto: ', [validators.DataRequired()])
	street = StringField('Ulice: ', [validators.DataRequired()])
	zipcode = StringField('PSČ: ', [validators.DataRequired()])

	profile = FileField('Profile photo', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please')])

	submit = SubmitField('Registrovat')

	def validate_username(self, username):
		if Register.query.filter_by(username=username.data).first():
			raise ValidationError(f"Přihlašovací jméno {username.data} je již obsazeno.")

	def validate_email(self, email):
		if Register.query.filter_by(username=email.data).first():
			raise ValidationError(f"Tento email {email.data} je již obsazen.")

	def validate_contact(self, contact):
		if Register.query.filter_by(username=contact.data).first():
			raise ValidationError(f"Telefonní číslo {contact.data} je již obsazeno.")


class CostumersLoginForm(FlaskForm):
	email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
	password = PasswordField('Password: ', [validators.DataRequired()])





