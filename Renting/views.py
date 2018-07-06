#! -*- coding:utf-8 -*-

from Renting import app
from flask import render_template, request, redirect,flash,get_flashed_messages
from models import User


@app.route('/')
def index():
    return render_template('index.html')


#登录功能的实现
@app.route('/login/')
def login():
    username = request.values.get('user_login')
    password = request.values.get('pass_login')

    user = User.query.filter_by(username=username)

    #转到注册页面
    #if user == None:
    #    return redirect('/reg/')
    #else:
    if password == user.password:
        print("登录成功")