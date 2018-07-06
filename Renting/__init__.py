#! -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('app.conf')
app.secret_key = "renting"
db = SQLAlchemy(app)

from Renting import views, models