from authors_app import db
from datetime import datetime
from flask_bcrypt import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.Integer, unique=True)
    user_type = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    biography = db.Column(db.Text, nullable=True) 
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Use a different backref name, such as 'user_books'
    user_books = db.relationship('Book', backref='user_books', lazy=True)

    def __init__(self, first_name, last_name, email, contact, user_type, password, biography, image=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.user_type = user_type
        self.password = password
        self.image = image
        self.biography = biography

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"
        
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
    
    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
