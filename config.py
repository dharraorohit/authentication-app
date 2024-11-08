import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'api.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'f5094db7dc611ba7464fff5bed3bbb6911a9766f'
    TOKEN_EXPIRY_DAYS = os.environ.get('TOKEN_EXPIRY_DAYS', 0)
    TOKEN_EXPIRY_HOURS = os.environ.get('TOKEN_EXPIRY_HOURS', 0)
    TOKEN_EXPIRY_MIN = os.environ.get('TOKEN_EXPIRY_MIN', 10)


app_config = {
    'default': Config
}
