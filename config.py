import os

class Config:
    SECRET_KEY = os.getenv('FLASKBLOG_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASKBLOG_SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('EMAIL')
    MAIL_PASSWORD = os.getenv('EMAIL_PWD')