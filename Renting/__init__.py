#! -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('app.conf')
app.secret_key = "renting"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = '/login/'                 #未登录状态不能访问的页面，自动跳转登录页面

from Renting import views, models