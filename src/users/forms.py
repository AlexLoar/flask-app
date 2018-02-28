from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class UserForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=-1, max=20, message='You can not have more than 20 characters')])
    email = StringField('E-mail', validators=[Email(), Length(min=-1, max=80, message='You can not have more than 80 characters')])
    age = IntegerField('Age', validators=[NumberRange(min=-1, max=99, message='Age must be a positive integer lower than 99')])
    phone = StringField('Phone', validators=[NumberRange(min=-1, message='Phone can not have more than 20 characters')])
    location = StringField('Location', validators=[Length(min=-1, max=80, message='Location can not have more than 80 characters')])
