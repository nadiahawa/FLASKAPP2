#object relational mapper - ORM 

import email
from click import password_option
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL, PrimaryKeyConstraint

db = SQLAlchemy()


from flask_login import LoginManager, UserMixin
login = LoginManager()

@login.user_loader
def load_user(userid):
    return User.query.get(userid)


from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255), default='No bio.')
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    api_token = db.Column(db.String(100))
    posts = db.relationship('Post', backref ='post_author') #tells user model taht it has a relationshop with the post model 

    def __init__(self, username, email, password, first_name='', last_name=''):
        self.username = username
        self.email = email.lower()
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.id = str(uuid4())
        self.password = generate_password_hash(password)


class Animal(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    species = db.Column(db.String(50), nullable = False)
    latin = db.Column(db.String(255), default=None)
    size_cm = db.Column(db.Integer)
    image = db.Column(db.String(100), default=None)
    price = db.Column(db.Float(2), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, dict):
        self.id = str(uuid4())
        self.species = dict['species'].title()
        self.description = dict['description']
        self.price = dict['price']
        self.image = dict.get('image')
        self.size_cm = dict.get('size_cm', 0)
        self.latin = dict.get('latin', 'unknown')[0].upper() + dict.get('latin', 'unknown')[1:].lower()
        

    def to_dict(self):
        return {
            'id' : self.id,
            'species' : self.species,
            'latin' : self.latin,
            'image' : self.image,
            'size': self.size_cm,
            'price' : self.price,
            'description' : self.description
        }

    def from_dict(self, dict):
        self.latin = dict.get('latin')
#  'price' : self.price,
# 'description' : self.description
# 'species' : self.species,

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable = False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    author = db.Column(db.String, db.ForeignKey('user.id'))
