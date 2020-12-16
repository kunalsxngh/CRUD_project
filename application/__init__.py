from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config['SECRET_KEY']= "SOME_KEY"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@35.246.0.15/crud_db"

db = SQLAlchemy(app)

from application import routes