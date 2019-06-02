from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo 


class GuviRegistration(FlaskForm):
	username = StringField('UserName' , validators = [DataRequired(), 
										Length(min=2,max=20)])
	email = StringField('Email' , validators = [DataRequired(), 
										Email()])
	password = PasswordField('Password' , validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password' , validators = [DataRequired() , EqualTo('password')])
	submit = SubmitField('Sign Up')

class GuviLogin(FlaskForm):
	email = StringField('UserName' , validators = [DataRequired(), 
										Email()])
	password = PasswordField('Password' , validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class PersonalDetails(FlaskForm):
	dob = DateField('DatePicker', format='%Y-%m-%d')
	contact = IntegerField('Contact', validators = [DataRequired()])
	age = IntegerField('Age', validators = [DataRequired()])
	submit = SubmitField('Save')