from authors_app import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True) 
    industry = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  
    #user = db.relationship('User', backref='companies')  
    created_at = db.Column(db.DateTime, default=datetime.now)  
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)  # Corrected DateTime spelling

    def __init__(self, name, industry, location):
        self.name = name
        self.industry = industry
        self.location = location
        # self.user_type = user_type

    def __repr__(self):
        return f"{self.name} {self.location}"
