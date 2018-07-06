# -*- encoding=UTF-8 -*-

from Renting import app, db
from Renting.models import User
from flask import render_template, request, flash, get_flashed_messages, redirect
from flask_login import login_user, logout_user, current_user, login_required
import random, hashlib


@app.route('/', methods={'post', 'get'})
def index():
    return render_template('index.html')


def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/reg/', methods={'post', 'get'})
def reg():
    #request.args
    #request.form
    username = request.values.get('user_sign').strip()
    password = request.values.get('pass_sign').strip()
    repeat_password = request.values.get('pass_repeat').strip()
    email = request.values.get('email').strip()

    print(username)
    if username == '' or password == '' or repeat_password == '' or email == '':
        return redirect_with_msg('/', u'不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()
    if user != None:
        return redirect_with_msg('/', u'用户名已经存在', 'reglogin')

    if password != repeat_password:
        return redirect_with_msg('/', u'两次输入密码不相同', 'reglogin')

    salt = '.'.join(random.sample('0123456789ABCdef', 10))
    m = hashlib.md5()
    m.update((password + salt).encode('utf8'))
    password = m.hexdigest()
    user = User(username, password, email, salt)
    db.session.add(user)
    db.session.commit()

    return redirect('/')

#登录功能的实现
@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('user_login').strip()        #得到输入框的用户名
    password = request.values.get('pass_login').strip()        #得到输入框的密码

    #输入的用户名或者密码为空
    if username == '' or password == '':
        return redirect('/index/')

    user_database = User.query.filter_by(username=username).first()

    #用户名不存在
    if user_database == None:
        return redirect('/index/')

    if user_database.password == password:
        print("登录成功")

    return redirect('/')

