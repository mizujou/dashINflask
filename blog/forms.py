from flask_wtf import FlaskForm
from wtforms import StringField
import wtforms
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from blog.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first() # Check if the username already exist
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists. Please try a different one')

    username = StringField(label='Pseudo / Username:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()]) # Check if the email is correct
    password1 = PasswordField(label='Mot de Passe:', validators=[Length(min=6, max=99), DataRequired()])
    password2 = PasswordField(label='Confirmation du Mot de Passe:', validators=[EqualTo('password1'), DataRequired()]) # Check if the password1 and 2 are the same
    submit = SubmitField(label='Create Account') 

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell')