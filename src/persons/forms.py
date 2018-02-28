from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, DateField, IntegerField
from wtforms.validators import DataRequired, Length


class PartyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=-1, max=20, message='You can not have more than 20 characters')])
    location = StringField('Location', validators=[Length(min=-1, max=80, message='Location can not have more than 80 characters')])
    date = DateField('Date')
    guests = SelectMultipleField('Guests')

