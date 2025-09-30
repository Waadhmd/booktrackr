from data_models import db, Author, Book
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import DeclarativeBase


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

# Now initialize the db with the app
db.init_app(app)


#with app.app_context():
 #   db.create_all()
