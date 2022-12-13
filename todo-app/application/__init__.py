from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db' # for mysql: mysql+pymysql://<username>:<password>@<host>:3306/<database>
# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = getenv('SECRET_KEY')

db = SQLAlchemy(app)

import application.routes