from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column,Text,ForeignKey
from datetime import datetime
from . import User
class Articles(db.Model):
    id = Column(Integer(), primary_key=True)
    subject = Column(String(150))
    content = Column(Text)
    writer = Column(Integer , ForeignKey('users.id'))
    thumb = Column(String(150 ) , default = '')
    views = Column(Integer , default = 0)
    publish = Column(Boolean , default = False)
    category_id = Column(Integer , ForeignKey('category.id'))
    created_at = Column(DateTime , default = datetime.utcnow())
    
    def getWriter(self):
        user = User.Users.query.filter(User.Users.id == self.writer).first()
        return user.username
    

class Comments(db.Model):
    id = Column(Integer , primary_key=True)
    user_id = Column(Integer , ForeignKey('users.id'))
    article_id = Column(Integer , ForeignKey('articles.id'))
    text = Column(Text)
    status = Column(Boolean , default = False)
    created_at = Column(DateTime , default = datetime.utcnow())


    def getWriter(self):
        user = User.Users.query.filter_by(id = self.user_id).first()
        return user.username
    
    def getArticle(self):
        article = Articles.query.filter_by(id = self.article_id).first()
        return article.subject
    
class Category(db.Model):
    id = Column(Integer , primary_key=True)
    name = Column(String(100))