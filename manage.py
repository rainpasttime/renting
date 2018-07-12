#! -*- coding:utf-8 -*-

from Renting import app, db
from flask_script import Manager
from Renting.models import House, User

manager = Manager(app)


@manager.command             #初始化数据库
def init_database():
    db.drop_all()             # 把所有数据类删除
    db.create_all()           # 把所有数据类创建
    # db.session.add(User('user1', 'user1', 'ss', ' '))

    # for i in range(0, 10):
    #     db.session.add(House(i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, 'user1', 1))

    # db.session.commit()


if __name__ == '__main__':
    manager.run()
