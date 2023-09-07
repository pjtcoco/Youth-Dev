from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, URL
from email_validator import validate_email
from flask_wtf.file import FileAllowed
from wtforms.fields.simple import MultipleFileField

class MentorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    github_link = StringField('GitHub Account', validators=[DataRequired(), URL()])
    organization = StringField('Organization', validators=[DataRequired()])
    images = MultipleFileField('Images', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    age = IntegerField('Age', validators=[DataRequired()]) 
    gender = SelectField('Gender', choices=[('female', 'Female'), ('male', 'Male')], validators=[DataRequired()])
    submit = SubmitField('Submit')


class MenteeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    organization = StringField('Organization')
    age = IntegerField('Age', validators=[DataRequired()])
    education_level = StringField('Education Level', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'Select Gender'),('Male', 'Male'),('Female', 'Female'),
    ], validators=[DataRequired()])
    program_studied = StringField('Program Studied', validators=[DataRequired()])
    images = MultipleFileField('Images', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])