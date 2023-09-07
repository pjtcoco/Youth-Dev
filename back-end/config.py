from flask import Flask
import os
from flask_wtf.csrf import CSRFProtect
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

class Config:
    SECRET_KEY = os.urandom(32)
    default_filepath = os.getcwd()
    print(default_filepath)
    app.config['SECRET_KEY'] = '32'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Zonecoco2003.@localhost:5432/youthdev'
    app.config['UPLOAD_FOLDER'] = 'C:/Users/user/Desktop/pictures'
    app.config['MENTORS_PER_PAGE'] = 5  # Set the desired number of mentors per page
    app.config['MENTEES_PER_PAGE'] = 5  # Set the desired number of mentees per page
    # template_loader = FileSystemLoader('templates')
    # app.jinja_env = Environment(loader=template_loader)
    app.jinja_env.globals['enumerate'] = enumerate

csrf = CSRFProtect(app)