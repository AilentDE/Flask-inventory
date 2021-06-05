from types import CoroutineType
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from datetime import datetime

from booking.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")

class RegisterRequestForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Invite")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("email address already registered")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat_password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Existed username')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Existed email')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Request")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Wrong email address")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat_password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")

class BookingForm(FlaskForm):
    shipping_method = SelectField("Shipping method", choices=[('airmail', 'Airmail'), ('ePacket', 'ePacket'), ('EMS', 'EMS'), ('FedEx', 'FedEx')])
    order_number = StringField("Order #")
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name")
    phone = StringField("Phone number", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state_code = StringField("State code")
    postcode = StringField("Postcode(ZIP)", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    remark = StringField("Remark")

    sku = StringField("SKU", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Send")

class ReportForm(FlaskForm):
    order_number = StringField("Order #")
    tracking_number = StringField("Tracking #")
    shipping_date = DateTimeField("Shipping Date")
    delivery_fee = IntegerField("Delivery Fee")
    materials_fee = IntegerField("Materials Fee")
    package_weight = IntegerField("Package Weight")
    submit = SubmitField("Report_Update")