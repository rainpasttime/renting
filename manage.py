#! -*- coding:utf-8 -*-

from Renting import app, db
from flask_script import Manager
from Renting.models import User

manager = Manager(app)


@manager.command             #初始化数据库
def init_database():
    db.drop_all()             #把所有数据类删除
    db.create_all()          #把所有数据类创建
    for i in range(10):
        phone = int(i)
        db.session.add(User( "username"+str(i), "password"+str(i), "email"+str(i), phone))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
