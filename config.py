import os


class Config(object):
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'b77069f5809ce4'
    MAIL_PASSWORD = 'fa94ef1f5debb1'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'blog.db')
    UPLOAD_DIR = os.path.curdir = 'static/uploads/'
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Config Recaptcha
    RECAPTCHA_PUBLIC_KEY = '6LdwvkwaAAAAAPBGpUj2hCPw7rZMWbGGpuKBdULn'
    RECAPTCHA_PRIVATE_KEY = '6LdwvkwaAAAAAIFv3eesWhFmgdeiTNy-tlCgqkoB'
    

class ProductionConfig(Config):
    DEBUG = True
    pass

class DevelopmentConfig(Config):
    pass
