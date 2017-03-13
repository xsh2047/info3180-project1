from wtforms import Form, StringField, TextAreaField, IntegerField, SelectField, validators
from flask_wtf.file import FileField

class ProfileForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=4, max=25), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=4, max=25), validators.DataRequired()])
    age = IntegerField('Age', [validators.DataRequired()])
    bio = TextAreaField('Bio', [validators.Length(min=0, max=125)])
    gender = SelectField('Sex', choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')])
