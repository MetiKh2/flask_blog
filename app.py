from models import User
from flask import Flask, render_template, request, redirect, url_for, flash, abort, __version__
from validators.auth import LoginForm, RegisterForm
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash
import os
from flask_login import LoginManager, login_user, current_user, logout_user
from controller import home, user, auth, admin, article
from db_manager import db
from flask_mail import Mail
from flask_moment import Moment
from mail_manager import mail
app = Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY')
if app.config['ENV']=='production' :
    app.config.from_object('config.ProductionConfig')
else :
    app.config.from_object('config.DevelopmentConfig')
    

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


login = LoginManager()
login.login_view = 'Login'
login.login_message_category = 'info'
login.init_app(app)


@login.user_loader
def userLoader(user_id):
    return db.session.query(User.Users).get(user_id)


db.init_app(app)
with app.app_context():
    db.create_all()

mail.init_app(app)

UPLOAD_DIR = os.path.curdir = 'static/uploads/'


app.secret_key = '1dae11441a1a2acf1cad3eca'
app.jinja_env.line_statement_prefix = '@'


moment = Moment(app=app)

homeController = home.Home()
userController = user.Account()
authController = auth.Auth()
adminController = admin.Admin()
articleController = article.Article()


app.add_url_rule('/', 'main', homeController.main)

app.add_url_rule('/article/<int:id>', 'single',
                 homeController.single, methods=['GET', 'POST'])


app.add_url_rule('/register', 'Register',
                 authController.Register, methods=['GET', 'POST'])

app.add_url_rule('/login', 'Login', authController.Login,
                 methods=['GET', 'POST'])

app.add_url_rule('/signout', 'SignOut',
                 authController.SignOut, methods=['GET', 'POST'])

app.add_url_rule('/forget', 'forget', authController.forget,
                 methods=['GET', 'POST'])

app.add_url_rule('/resetpassword/<token>/<user_id>', 'reset_password',
                 authController.reset_password, methods=['GET', 'POST'])

app.add_url_rule('/account', 'Account', userController.Account)

app.add_url_rule('/account_info', 'AccountInfo', userController.AccountInfo)

app.add_url_rule('/changepassword', 'ChangePassword',
                 userController.ChangePassword, methods=['GET', 'POST'])

app.add_url_rule('/account_edit', 'AccountEdit',
                 userController.AccountEdit, methods=['GET', 'POST'])

app.add_url_rule('/account_avatar', 'AccountAvatar',
                 userController.AccountAvatar, methods=['GET', 'POST'])

app.add_url_rule('/admin', 'Index', adminController.Index)

app.add_url_rule('/admin/user', 'get_all_users',
                 adminController.get_all_users, methods=['POST', 'GET'])

app.add_url_rule('/admin/user/add', 'add_user',
                 adminController.add_user, methods=['POST', 'GET'])

app.add_url_rule('/admin/user/edit', 'edit_user',
                 adminController.edit_user, methods=['POST', 'GET'])

app.add_url_rule('/admin/post/add', 'create_post',
                 articleController.create_post, methods=['POST', 'GET'])

app.add_url_rule('/admin/post', 'get_all_articles',
                 articleController.get_all_articles, methods=["POST", 'GET'])

app.add_url_rule('/admin/post/edit', 'edit_post',
                 articleController.edit_post, methods=['POST', 'GET'])

app.add_url_rule('/admin/comments', 'get_all_comments',
                 adminController.get_all_comments, methods=['GET'])

app.add_url_rule('/admin/comments/approve/<int:comment_id>',
                 'approve_comment', adminController.approve_comment, methods=['POST'])

app.add_url_rule('/admin/comments/delete/<int:comment_id>',
                 'delete_comment', adminController.delete_comment, methods=['POST'])

app.add_url_rule('/admin/category/add', 'create_category',
                 articleController.create_category, methods=['POST', 'GET'])

app.add_url_rule('/admin/category', 'get_all_categories',
                 articleController.get_all_categories, methods=["POST", 'GET'])

app.add_url_rule('/admin/category/edit', 'edit_category',
                 articleController.edit_category, methods=['POST', 'GET'])

app.add_url_rule('/category/<string:name>', 'view_category',
                 articleController.view_category, methods=['GET'])

app.add_url_rule('/search', 'search', articleController.search)

# categories=db.session.query(article.Category).all()
# app.jinja_env.globals['categories']=article.Category.query.all()


@app.template_filter('subContent')
def subContent(content):
    return content[0:100]+'...'


@app.context_processor
def inject_stage_and_region():
    return dict(categories=db.session.query(article.Category).all())


app.jinja_env.filters['subContent'] = subContent

# @app.errorhandler(404)
# def NotFound(error):
#     return render_template('404.html',error=error)
if __name__ == '__main__':
    app.run()
