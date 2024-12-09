from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False)
  role = db.Column(db.String(80), nullable=False, default='user')
  
  meals = db.relationship('Meals', backref='user', lazy=True, cascade='all, delete-orphan')

