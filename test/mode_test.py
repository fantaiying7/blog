import os
import sys

sys.path.append(os.path.realpath(__file__ + "/../.."))

from flask.app import Flask
import random
import string
import unittest
from blog.models.exts import db, bcrypt
from blog.models.modetool import *
from blog.models.mode import *


config = 'conf.flask.config.DevelopmentConfig'


app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)
bcrypt.init_app(app)


def random_str(num, userstr=""):
    str_pool = userstr if userstr else string.ascii_letters + string.digits
    if len(str_pool) < num:
        str_pool *= num // len(str_pool) + 1
    return ''.join(random.sample(str_pool, num))

class TestModeTools(unittest.TestCase):

    def test_001_create_db(self):
        with app.app_context():
            creat_db()

    def test_002_modeapi(self):
        with app.app_context():
            user_api = Database(User)
            name = random_str(10)
            domainname01 = f"{random_str(10, string.digits)}.com"
            # 添加
            user_data = {
                "name": name,
                "password": "test_pwd",
                "email": f"{random_str(10, string.digits)}@qq.com",
                "domainname": domainname01,
                "telephone": random_str(11, string.digits),
                "nickname": "二猫子",
            }
            user_api.insert(user_data)

            condition = {"name": name}
            result = ["id", "domainname"]

            data = user_api.select(condition, result)[-1]
            id = data["id"]
            domainname = data["domainname"]
            self.assertEqual(domainname, domainname01)

            # 检查密码
            self.assertTrue(user_api.check_password_for_name(name, "test_pwd"))
            self.assertFalse(user_api.check_password_for_name(name, "test_pwd_123"))

            # 查询空字典
            data = user_api.select()
            self.assertTrue(data)

            # 更新
            condition = {"id": id}
            domainname02 = f"{random_str(10, string.digits)}.com"
            user_api.update({"id": id}, {"domainname": domainname02})

            data = user_api.select(condition, result)[-1]
            domainname = data["domainname"]
            self.assertEqual(domainname, domainname02) 

            # 删除
            data = user_api.select(condition, result)[-1]
            domainname = data["domainname"]
            user_api.delete(condition)

            data = user_api.select(condition, result)
            self.assertFalse(data) 

class TestTabal(unittest.TestCase):

    def test_001_user(self):
        pass


if __name__ == '__main__':
    unittest.main()