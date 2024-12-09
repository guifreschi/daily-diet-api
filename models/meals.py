from database import db
from datetime import datetime, timezone

class Meals(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date_time = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    on_diet = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
