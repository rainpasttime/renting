# -*- encoding=UTF-8 -*-

from Renting import app, db
from Renting.models import User, Order, House
from flask import render_template, request, flash, get_flashed_messages, redirect
from flask_login import login_user, logout_user, current_user, login_required
import random
import hashlib


@app.route('/index/', methods={'post', 'get'})
@app.route('/', methods={'post', 'get'})
def index():
    return render_template('index.html')


#个人中心页面 带有一个参数user表示现在的user
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    return render_template('profile.html', user=user)


def redirect_with_msg(target, msg, category):
    if msg is not None:
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

    user_check = User.query.filter_by(username=username).first()
    if user_check is not None:
        return redirect_with_msg('/', u'用户名已经存在', 'reglogin')

    if password != repeat_password:
        return redirect_with_msg('/', u'两次输入密码不相同', 'reglogin')

    salt = '.'.join(random.sample('0123456789ABCdef', 10))
    m = hashlib.md5()
    m.update((password + salt).encode('utf8'))
    password = m.hexdigest()
    user_get = User(username, password, email, salt)
    db.session.add(user_get)
    db.session.commit()
    print("user_get:"+str(type(user_get)))
    login_user(user_get)

    next_page = request.values.get('next')
    if next_page is not None and next_page.startswith('/') > 0:
        return redirect(next_page)
    return redirect('/')


#登录功能的实现
@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('user_login').strip()        #得到输入框的用户名
    password = request.values.get('pass_login').strip()        #得到输入框的密码


    #输入的用户名或者密码为空
    if username == '' or password == '':
        print("one")
        return redirect_with_msg('/index/', u'用户名和密码不能为空', 'login')

    user_database = User.query.filter_by(username=username).first()

    #用户名不存在
    if user_database == None:
        print("用户名不存在")
        return redirect_with_msg('/index/',u'用户名不存在', 'login')

    m = hashlib.md5()
    m.update((password + user_database.salt).encode('utf8'))
    if m.hexdigest() != user_database.password:
        print("密码错误")
        return redirect_with_msg('/index/', u'密码错误', 'login')

    login_user(user_database)
    print("登录成功")

    next_page= request.values.get('next')
    if next_page is not None and next_page.startswith('/') > 0:
        return redirect(next_page)
    return redirect('/')


#用户登出
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/index/')


@app.route('/renting/')
def history():
    '''先得到目前的用户
        然后从数据库中查询这个用户的所有订单
    '''
    #得到这个用户的作为买家的所有订单
    user = current_user
    result_renter = []
    renter_list = Order.query.filter_by(renter=user.username).all()
    for item in renter_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        print(one)
        result_renter.append(one)
    #返回的是list类型
    return render_template('renting.html', result_renter=result_renter)


@app.route('/release/', methods={'post', 'get'})
def release():
    '''显示房屋发布界面'''
    return render_template('release.html')


@app.route('/release_buttom/', methods={'post', 'get'})
def release_buttom():
    house_name = request.values.get('house_name').strip()
    tem = request.values.get('rent_type').strip()
    print("house" + house_name)

    if tem == '整租':
        house_type = 0
    elif tem == '单间':
        house_type = 1
    else:
        house_type = 2

    area = int(request.values.get('area').strip())
    people = int(request.values.get('people').strip())
    bedroom = int(request.values.get('bedroom').strip())
    toilet = int(request.values.get('toilet').strip())

    tem = request.values.get('kitchen').strip()
    if tem == "有":
        kitchen = 1
    else:
        kitchen = 0

    bed = int(request.values.get('bed').strip())

    tem = request.values.get('bed_type').strip()
    if tem == "单人床":
        bed_type = 0
    else:
        bed_type = 1

    description = request.values.get('description').strip()
    price = int(request.values.get('price').strip())
    facility =""
    tem = request.values.get('TV').strip()
    if tem == "有":
        facility = facility+"1"
    else:
        facility = facility + "0"
    tem = request.values.get('fridge').strip()
    if tem == "有":
        facility = facility + "1"
    else:
        facility = facility + "0"
    tem = request.values.get('washer').strip()
    if tem == "有":
        facility = facility + "1"
    else:
        facility = facility + "0"
    tem = request.values.get('conditioner').strip()
    if tem == "有":
        facility = facility + "1"
    else:
        facility = facility + "0"
    tem = request.values.get('wifi').strip()
    if tem == "有":
        facility = facility + "1"
    else:
        facility = facility + "0"
    tem = request.values.get('heater').strip()
    if tem == "有":
        facility = facility + "1"
    else:
        facility = facility + "0"
    tem = request.values.get('wardrobe').strip()
    if tem == "有":
        facility = facility + "1"
    else:
        facility = facility + "0"
    tem = request.values.get('parking').strip()
    if tem == "有":
        facility = facility + "1"
    else:
        facility = facility + "0"

    province = request.values.get('province').strip()
    city = request.values.get('city').strip()
    district = request.values.get('district').strip()
    address = request.values.get('address').strip()

    user = current_user

    house = House(house_name, house_type, area, people, bedroom, toilet, kitchen, bed, bed_type, price, description,
                  facility, province, city, district, address, user.username)

    db.session.add(house)
    db.session.commit()

    all_house = House.query.filter_by(username=user.username).all()
    return render_template('myhouse.html', house=all_house)


@app.route('/myhouse/')
def myhouse():
    '''根据当前用户查询房屋表，得到这个用户的房屋信息返回给前端'''
    user = current_user
    house = House.query.filter_by(username=user.username).all()
    return render_template('myhouse.html', house=house)

