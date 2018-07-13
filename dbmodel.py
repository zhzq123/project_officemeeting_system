from sqlalchemy import Column, Integer, String
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
import time
import random


class User(Base):
    __tablename__ = 'users'
    name = Column(String(20), nullable=False)
    hash_password = Column(String(128), nullable=False)
    email = Column(String(20), primary_key=True, unique=True)
    confirm = Column(Integer)
    reg_time = Column(Integer)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.hash_password = generate_password_hash(password)
        self.reg_time = int(time.time())
        self.confirm = random.randint(-1e15, 1e15)
        while self.confirm == 0:
            self.confirm = random.randint(-1e15, 1e15)

    def setconfrim(self):
        self.confirm = random.randint(-1e15, 1e15)
        while self.confirm == 0:
            self.confirm = random.randint(-1e15, 1e15)

    def reset_pasword(self, password):
        self.hash_password = generate_password_hash(password)

    def judge_password(self, password):
        return check_password_hash(self.hash_password, password)

    def __repr__(self):
        return u"< {0} , {1},{2} >".format(self.name, self.email,
                                           self.hash_password)
