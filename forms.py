from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class SignupForm(FlaskForm):
	account_name = StringField('Enter Account Name', validators=[DataRequired("Please enter your account name")])
	account_password = PasswordField('Enter Password', validators=[Length(min=6), DataRequired("Passwords must be a minimum of 6 characters. Use at least one letter, number and special character.")])
	submit = SubmitField('Sign Up')

class SigninForm(FlaskForm):
	user_name = StringField('Username', validators=[DataRequired("Please enter your username")])
	user_password = PasswordField('Password', validators=[Length(min=6), DataRequired("Passwords must be a minimum of 6 characters. Use at least one letter, number and special character.")])
	submit = SubmitField('Sign In')

class AddressForm(FlaskForm):
	address = StringField('Address', validators=[DataRequired("Please enter an address.")])
	submit = SubmitField('Search')