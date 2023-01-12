from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from vadhyakalakshethra.models import *
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SelectField




class AddVadhyam(FlaskForm):
    name = StringField('Vadhyam',validators=[DataRequired()])
    type = StringField('Type',validators=[DataRequired()])
    material = StringField('Material', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    price = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')