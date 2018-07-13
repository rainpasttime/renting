# -*- encoding=UTF-8 -*-

from Renting import app, db
from Renting.models import User, Order, House
from flask import render_template, request, flash, get_flashed_messages, redirect,send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from Renting.page_utils import Pagination
import random
import hashlib
import uuid
import os
from datetime import date, datetime


@app.route('/index/', methods={'post', 'get'})
@app.route('/', methods={'post', 'get'})
def index():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('index.html', msg=msg)


# 个人中心页面 带有一个参数user表示现在的user
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
    # request.args
    # request.form
    username = request.values.get('user_sign').strip()
    password = request.values.get('pass_sign').strip()
    email = request.values.get('email').strip()

    user_check = User.query.filter_by(username=username).first()
    if user_check is not None:
        return redirect_with_msg('/', u'用户名已经存在', 'reglogin')
    user_check = User.query.filter_by(email=email).first()
    if user_check is not None:
        return redirect_with_msg('/', u'邮箱已经存在', 'reglogin')


    salt = '.'.join(random.sample('0123456789ABCdef', 10))
    m = hashlib.md5()
    m.update((password + salt).encode('utf8'))
    password = m.hexdigest()
    user_get = User(username, password, email, salt)
    db.session.add(user_get)
    db.session.commit()

    login_user(user_get)

    next_page = request.values.get('next')
    if next_page is not None and next_page.startswith('/') > 0:
        return redirect(next_page)

    return redirect('/')


# 登录功能的实现
@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('user_login').strip()        # 得到输入框的用户名
    password = request.values.get('pass_login').strip()        # 得到输入框的密码
    # 输入的用户名或者密码为空

#    if username == '' or password == '':
#       return redirect_with_msg('/', u'用户名和密码不能为空', 'reglogin')

    user_database = User.query.filter_by(username=username).first()

    # 用户名不存在
    if user_database is None:
        return redirect_with_msg('/', u'用户名不存在', 'reglogin')

    m = hashlib.md5()
    m.update((password + user_database.salt).encode('utf8'))
    if m.hexdigest() != user_database.password:
        return redirect_with_msg('/', u'密码错误', 'reglogin')

    login_user(user_database)

    next_page = request.values.get('next')
    if next_page is not None and next_page.startswith('/') > 0:
        return redirect(next_page)
    return redirect('/')


# 用户登出
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/index/')


@app.route('/renting/')
def history():
    # 先得到目前的用户然后从数据库中查询这个用户的所有订单
    # 得到这个用户的作为买家的所有订单
    now_compare = datetime.now().date()
    user = current_user
    result_renter = []
    renter_list = Order.query.filter_by(renter=user.username).all()
    for item in renter_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        if now_compare < item.start_time and item.status == 1:
            one['cancel'] = 1
        else:
            one['cancel'] = 0
        print(one)
        result_renter.append(one)
    # 返回的是List类型
    return render_template('renting.html', result_renter=result_renter)


@app.route('/housedes/<int:house_id>/')
def house_des(house_id):
    house = House.query.filter_by(id=house_id).first()
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['message']):
        msg = msg + m
    return render_template('housedescription.html', house=house, msg=msg)


@app.route('/makeorder/<int:house_id>/', methods={'get', 'post'})
def make_order(house_id):
    house = House.query.filter_by(id=house_id).first()
    seller = house.username
    starttime = request.values.get('datepicker')
    endtime = request.values.get('datepicker1')

    startyear = int(starttime[6]) * 1000 + int(starttime[7]) * 100 + int(starttime[8]) * 10 + int(starttime[9])
    startmonth = int(starttime[0]) * 10 + int(starttime[1])
    startday = int(starttime[3]) * 10 + int(starttime[4])
    startdate = date(startyear, startmonth, startday)

    endyear = int(endtime[6]) * 1000 + int(endtime[7]) * 100 + int(endtime[8]) * 10 + int(endtime[9])
    endmonth = int(endtime[0]) * 10 + int(endtime[1])
    endday = int(endtime[3]) * 10 + int(endtime[4])
    enddate = date(endyear, endmonth, endday)

    if startdate > enddate:
        return redirect_with_msg('/housedes/' + str(house_id) + '/', u'住房时间比退房时间晚，预订失败', 'message')
    elif not current_user.is_authenticated:
        return redirect_with_msg('/housedes/' + str(house_id) + '/', u'请先登陆', 'message')

    print(current_user)
    renter = current_user.username
    day = (enddate - startdate).days
    status = 1
    total_price = house.price * day

    # 判断以往订单时间上是否有冲突
    house_order = Order.query.filter_by(house_id=house_id).all()
    for order in house_order:
        if (startdate <= order.start_time <= enddate) or (startdate <= order.end_time <= enddate):
            return redirect_with_msg('/housedes/' + str(house_id) + '/', u'该时间与已知订单冲突，预订失败', 'message')

    new_order = Order(house_id, seller, renter, startdate, enddate, total_price, status)
    db.session.add(new_order)
    db.session.commit()

    return redirect_with_msg('/housedes/' + str(house_id) + '/', u'预订成功', 'message')


@app.route('/mainpage/')
def mainpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['research']):
        msg += m
    house_list = House.query.all()
    pager_obj = Pagination(request.args.get("page", 1), len(house_list), request.path, request.args, per_page_count=6)
    print(request.path)
    print(request.args)
    index_list = house_list[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template("mainpage.html", house=index_list, html=html, msg=msg)


@app.route('/search/', methods={'get', 'post'})
def search():
    province = request.values.get('prov5')
    city = request.values.get('city5')
    district = request.values.get('area5')
    price = request.values.get('price')
    print(province)
    print(city)
    print(district)
    print(price)

    if province is None or city is None or district is None:
        return redirect_with_msg('/mainpage/', u'请选择省，市，区进行搜索', 'research')

    house_list = House.query.filter_by(province=province, city=city, district=district).all()
    if price is not None:
        price = int(price)
        house_newlist = []
        for house in house_list:
            if price != 10000 and price - 100 < house.price <= price:
                house_newlist.append(house)
            elif price == 10000 and price > 500:
                house_newlist.append(house)
        pager_obj = Pagination(request.args.get("page", 1), len(house_newlist), request.path, request.args,
                               per_page_count=6)
    else:
        pager_obj = Pagination(request.args.get("page", 1), len(house_list), request.path, request.args,
                               per_page_count=6)

    index_list = house_list[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template("mainpage.html", house=index_list, html=html)


def save_to_local(file, file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, file_name))
    return '../static/image/upload/'+file_name


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
    eqipment_list = request.values.getlist("eqipment")
    if "tv" in eqipment_list:
        facility = facility + "1"
    else:
        facility = facility + "0"
    if "icebox" in eqipment_list:
        facility = facility + "1"
    else:
        facility = facility + "0"
    if  "washer" in eqipment_list:
        facility = facility + "1"
    else:
        facility = facility + "0"
    if "conditioner" in eqipment_list:
        facility = facility + "1"
    else:
        facility = facility + "0"
    if "wifi" in eqipment_list:
        facility = facility + "1"
    else:
        facility = facility + "0"
    if "heater" in eqipment_list:
        facility = facility + "1"
    else:
        facility = facility + "0"
    if "wardrobe" in eqipment_list:
        facility = facility + "1"
    else:
        facility = facility + "0"
    if "parking" in eqipment_list:
        facility = facility + "1"
    else:
        facility = facility + "0"
    '''tem = request.values.get('TV').strip()
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
        facility = facility + "0"'''

    province = request.values.get('province').strip()
    city = request.values.get('city').strip()
    district = request.values.get('district').strip()
    address = request.values.get('address').strip()

    user = current_user

    file_list = request.files.getlist('file')
    file_ext = ''
    url_list = []

    for file in file_list:
        if file.filename.find('.') > 0:
            file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
        if file_ext in app.config['ALLOWED_EXT']:
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
            url = save_to_local(file, file_name)
            if url is not None:
                url_list.append(url)

    house = House(house_name, house_type, area, people, bedroom, toilet, kitchen, bed, bed_type, price, description,
            facility, province, city, district, address, user.username, url_list)
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


@app.route('/modify_house/<int:house_id>/')
def modify_house(house_id):
    house = House.query.filter_by(id=house_id).first()
    return render_template("modify_house.html", house=house)


@app.route('/modify_buttom/<int:house_id>/', methods={'post', 'get'})
def modify_buttom(house_id):
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

    file_list = request.files.getlist('file')
    file_ext = ''
    url_list = []

    for file in file_list:
        if file.filename.find('.') > 0:
            file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
        if file_ext in app.config['ALLOWED_EXT']:
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
            url = save_to_local(file, file_name)
            if url is not None:
                url_list.append(url)

    house = House.query.filter_by(id=house_id).first()
    db.session.delete(house)
    new_house = House(house_name, house_type, area, people, bedroom, toilet, kitchen, bed, bed_type, price,
                      description, facility, province, city, district, address, house.username, url_list)
    db.session.add(new_house)
    db.session.commit()
    all_house = House.query.filter_by(username=house.username).all()
    return render_template('myhouse.html', house=all_house)


#用户取消订单的步骤
@app.route('/cancel_order/<int:order_id>/', methods={'post', 'get'})
def cancel_order(order_id):
    #得到订单
    order = Order.query.filter_by(id=order_id).first()
    new_order = Order(order.house_id, order.seller, order.renter, order.start_time, order.end_time, order.total_price, 3)
    db.session.delete(order)
    db.session.add(new_order)
    db.session.commit()

    now_compare = datetime.now().date()
    user = current_user
    result_renter = []
    renter_list = Order.query.filter_by(renter=user.username).all()
    for item in renter_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        if now_compare < item.start_time and item.status == 1:
            one['cancel'] = 1
        else:
            one['cancel'] = 0
        print(one)
        result_renter.append(one)
    # 返回的是List类型
    return render_template('renting.html', result_renter=result_renter)


#显示预定我的房子并且状态是已经受理或者已经取消的订单
@app.route('/rent_house/', methods={'post', 'get'})
def rent_myhouse():
    #得到订单
    username = current_user.username
    result_seller = []
    seller_list = Order.query.filter_by(seller=username, status=0).all()
    seller_list_two = Order.query.filter_by(seller=username, status=2).all()
    for item in seller_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        result_seller.append(one)
    for item in seller_list_two:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        result_seller.append(one)
    return render_template('rent_house.html', result_seller=result_seller)


#房主同意取消的操作
@app.route('/accept_cancel/<int:order_id>/', methods={'post', 'get'})
def accept_cancel_order(order_id):
    #得到订单
    order = Order.query.filter_by(id=order_id).first()
    new_order = Order(order.house_id, order.seller, order.renter, order.start_time, order.end_time, order.total_price, 0)
    db.session.delete(order)
    db.session.add(new_order)
    db.session.commit()

    username = current_user.username
    result_seller = []
    seller_list = Order.query.filter_by(seller=username).all()
    for item in seller_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        result_seller.append(one)
    return render_template('rent_house.html', result_seller=result_seller)


#房主拒绝取消的操作
@app.route('/refuse_cancel/<int:order_id>/', methods={'post', 'get'})
def refuse_cancel(order_id):
    #得到订单
    order = Order.query.filter_by(id=order_id).first()
    new_order = Order(order.house_id, order.seller, order.renter, order.start_time, order.end_time, order.total_price, 2)
    db.session.delete(order)
    db.session.add(new_order)
    db.session.commit()

    username = current_user.username
    result_seller = []
    seller_list = Order.query.filter_by(seller=username).all()
    for item in seller_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        result_seller.append(one)
    return render_template('rent_house.html', result_seller=result_seller)


#房主接受订单的操作
@app.route('/accept_order/<int:order_id>/', methods={'post', 'get'})
def accept_order(order_id):
    #得到订单
    order = Order.query.filter_by(id=order_id).first()
    new_order = Order(order.house_id, order.seller, order.renter, order.start_time, order.end_time, order.total_price, 2)
    db.session.delete(order)
    db.session.add(new_order)
    db.session.commit()

    username = current_user.username
    result_seller = []
    seller_list = Order.query.filter_by(seller=username).all()
    for item in seller_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        result_seller.append(one)
    return render_template('rent_house.html', result_seller=result_seller)


#房主拒绝受理的操作
@app.route('/refuse_order/<int:order_id>/', methods={'post', 'get'})
def refuse_order(order_id):
    #得到订单
    order = Order.query.filter_by(id=order_id).first()
    new_order = Order(order.house_id, order.seller, order.renter, order.start_time, order.end_time, order.total_price, 0)
    db.session.delete(order)
    db.session.add(new_order)
    db.session.commit()

    username = current_user.username
    result_seller = []
    seller_list = Order.query.filter_by(seller=username).all()
    for item in seller_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        result_seller.append(one)
    return render_template('rent_house.html', result_seller=result_seller)


#显示预定我的房子并且状态是已经受理或者已经取消的订单
@app.route('/operating/', methods={'post', 'get'})
def operating():
    #得到订单
    username = current_user.username
    result_seller = []
    seller_list = Order.query.filter_by(seller=username, status=1).all()
    seller_list_two = Order.query.filter_by(seller=username, status=3).all()
    for item in seller_list:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        result_seller.append(one)
    for item in seller_list_two:
        one = {}
        one_house = House.query.filter_by(id=item.house_id).first()
        one['order'] = item
        one['house'] = one_house
        result_seller.append(one)

    return render_template('operating.html', result_seller=result_seller)


@app.route('/modify_information/<int:user_id>/', methods={'post', 'get'})
def modify_information(user_id):
    new_name = request.values.get('name_modify').strip()
    new_email = request.values.get('email_modify').strip()
    new_phone = request.values.get('phone_modify').strip()
    new_password = request.values.get('password_modify').strip()
    old_user = User.query.filter_by(id=user_id).first()

    user_check = User.query.filter_by(username=new_name).first()
    if user_check is not None:
        return redirect_with_msg('/', u'用户名已经存在', 'reglogin')

    salt = '.'.join(random.sample('0123456789ABCdef', 10))
    m = hashlib.md5()
    m.update((new_password + salt).encode('utf8'))
    password = m.hexdigest()
    user_get = User(new_name, password, new_email, salt)
    user_get.phone_number = new_phone

    login_user(user_get)

    db.session.add(user_get)
    db.session.delete(old_user)
    db.session.commit()

    return redirect_with_msg('/', u'请重新登录', 'reglogin')
