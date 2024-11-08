import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import app_config

config_name = os.getenv('FLASK_ENV', 'default')

app = Flask(__name__)

app.config.from_object(app_config[config_name])
db = SQLAlchemy(app)

def create_tables():
    db.create_all()

migrate = Migrate(app, db, render_as_batch=True) # obj for db migrations
CORS(app)

import library.resources as resources
