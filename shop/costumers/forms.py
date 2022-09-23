from wtforms import Form, StringField,TextAreaField, PasswordField, SubmitField, validators
from flask_wtf.file import FileRequired, FileAllowed, FileField

class CostumerRegisterForm(Form):
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


