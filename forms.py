#Form templates are made in the form of classes which inherit from the Form class of WTForms library
#Various validators used to provide automatic validation in forms
#validators.Required: Means that field is required to be entered during form submission
#validators.Email: Checks entered value is in valid email address form
#validators.EqualTo: Checks the equality of two form fields, used to confirm entered password

from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, SelectField
from wtforms import validators, ValidationError

class RegistrationForm(Form):
    name=TextField("Name", [validators.Required()])
    username=TextField("Username", [validators.Required()])
    password=PasswordField("Password", [validators.Required()])
    confirm=PasswordField("Confirm Password", [validators.Required(), validators.EqualTo('password', message='Passwords do not match')])
    mail=TextField("E-Mail", [validators.Required(), validators.Email("Please enter valid email")])
    roll=TextField("Roll Number", [validators.Required()])
    submit=SubmitField("Submit")

class LoginForm(Form):
    username=TextField("Username", [validators.Required()])
    password=PasswordField("Password", [validators.Required()])
    submit=SubmitField("Submit")

class PreferenceForm(Form):
    p1=SelectField('Preference 1', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    p2=SelectField('Preference 2', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    p3=SelectField('Preference 3', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    p4=SelectField('Preference 4', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    p5=SelectField('Preference 5', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    p6=SelectField('Preference 6', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    p7=SelectField('Preference 7', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    p8=SelectField('Preference 8', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    p9=SelectField('Preference 9', choices=[('1','101'),('2','102'),('3','103'),('4','104'),('5','105'),('6','106'),('7','107'),('8','108'),('9','109')])
    submit=SubmitField("Submit")