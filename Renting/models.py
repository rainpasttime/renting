# -*-encoding:UTF-8 -*-
from Renting import db, login_manager
from datetime import datetime


# 用户表的定义
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID 用户唯一的标识
    username = db.Column(db.String(50), unique=True)  # 用户名  唯一   最大50个字符
    password = db.Column(db.String(100))  # 密码   最大100个字符
    phone_number = db.Column(db.Integer, unique=True)  # 手机号码
    email = db.Column(db.String(100), unique=True)  # 邮箱  唯一
    salt = db.Column(db.String(32))  # 密码加盐

    def __init__(self, username, password, email, salt):
        self.username = username
        self.password = password
        self.email = email
        self.salt = salt

    def __repr__(self):
        return '<User %d %s>' % (self.id, self.username)

    # Flask Login接口
    def is_authenticated(self):
        print('is_authenticated')
        return True

    def is_active(self):
        print('is_active')
        return True

    def is_anonymous(self):
        print('is_anonymous')
        return False

    def get_id(self):
        print('get_id')
        return self.id


# 管理员表的定义
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID 用户唯一的标识
    username = db.Column(db.String(10), unique=True)  # 用户名  唯一   最大10个字符
    password = db.Column(db.String(20))  # 密码   最大20个字符

    def __init__(self, username, password):
        self.username = username
        self.password = password


# 房屋表的定义
class House(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID 房屋唯一的标识
    house_name = db.Column(db.String(25))  # 房屋名  唯一   最大25个字符
    house_type = db.Column(db.Integer)  # 房屋类型，0表示整租，1表示单间 ，2表示床位
    area = db.Column(db.Integer)  # 房屋面积
    people = db.Column(db.Integer)  # 可住人数
    bedroom = db.Column(db.Integer)  # 卧房数
    toilet = db.Column(db.Integer)  # 卫生间数
    kitchen = db.Column(db.Integer)  # 是否有厨房
    bed = db.Column(db.Integer)  # 床位数
    bed_type = db.Column(db.Integer)  # 床型 0表示单人床  1表示双人床
    price = db.Column(db.Integer)  # 租一天的价格
    description = db.Column(db.String(200))  # 房屋描述
    facility = db.Column(db.String(10))  # 房屋设施，0表示无，1表示有
    province = db.Column(db.String(10))  # 省
    city = db.Column(db.String(10))  # 市
    district = db.Column(db.String(10))  # 地区
    address = db.Column(db.String(100))  # 具体地址
    username = db.Column(db.String(10), db.ForeignKey('user.username'))  # 房屋主人的名字，外键
    status = db.Column(db.Integer)  # 房屋状态，0表示未审核，1表示通过,2表示未通过
    url_one = db.Column(db.String(100))  # 房屋图片
    url_two = db.Column(db.String(100))  # 房屋图片
    url_three = db.Column(db.String(100))  # 房屋图片
    url_four = db.Column(db.String(100))  # 房屋图片
    url_five = db.Column(db.String(100))  # 房屋图片

    def __init__(self, house_name, house_type, area, people, bedroom, toilet, kitchen, bed, bed_type,
                 price, description, facility, province, city, district, address, username, url):
        self.house_name = house_name
        self.house_type = house_type
        self.area = area
        self.people = people
        self.bedroom = bedroom
        self.toilet = toilet
        self.kitchen = kitchen
        self.bed = bed
        self.bed_type = bed_type
        self.price = price
        self.description = description
        self.facility = facility
        self.province = province
        self.city = city
        self.district = district
        self.address = address
        self.username = username
        self.status = 0
        for i in range(len(url)):
            if i == 0:
                self.url_one = url[0]
            elif i == 1:
                self.url_two = url[1]
            elif i == 2:
                self.url_three = url[2]
            elif i == 3:
                self.url_four = url[3]
            else:
                self.url_five = url[4]


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 订单唯一的ID
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))  # 房屋ID 作为外键
    seller = db.Column(db.String(10), db.ForeignKey('user.username'))  # 房屋的卖家  作为外键
    renter = db.Column(db.String(10), db.ForeignKey('user.username'))  # 房屋租户  作为外键
    start_time = db.Column(db.Date)  # 订单开始时间
    end_time = db.Column(db.Date)  # 订单结束时间
    total_price = db.Column(db.Integer)  # 订单的价格
    status = db.Column(db.Integer)  # 订单状态 0表示订单已取消  1表示订单未受理  2表示订单受理  3表示订单正在取消

    def __init__(self, house_id, seller, renter, start_time, end_time, total_price, status):
        self.house_id = house_id
        self.seller = seller
        self.renter = renter
        self.start_time = start_time
        self.end_time = end_time
        self.total_price = total_price
        self.status = status


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

