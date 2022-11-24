from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Users(db.Model,UserMixin):
    id = Column(Integer(), primary_key=True)
    username = Column(String(), unique=True, nullable=False)
    email = Column(String())
    password = Column(String(),nullable=False)
    admin = Column(Boolean(),default=False)
    writer = Column(Boolean(),default=False)
    avatar = Column(String())
    phone = Column(String(),default='0')
    created_at = Column(DateTime(),default=datetime.utcnow())
    token=Column(String(),default='')

    @property
    def passwd(self):
        raise AttributeError('Access Forbidden')
    
    @passwd.setter
    def passwd(self , password):
        self.password = generate_password_hash(password)
    
    def IsOriginalPassword(self , user_password):
        return check_password_hash(self.password , user_password)



# from app import db
# from flask_sqlalchemy import Integer,String,DateTime,Boolean,Column
# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(110), unique=True, nullable=False)
#     email = db.Column(db.String(110))
#     password =db.Column(db.String(110),nullable=False)
#     admin =db.Column(db.Boolean(),default=False)
#     writer = db.Column(db.Boolean(),default=False)
#     avatar =db.Column(db.String(110))
#     phone = db.Column(db.String(20),default='0')
#     created_at = db.Column(db.DateTime())