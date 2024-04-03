from authors_app import db  # Assuming db is defined in authors_app package
from datetime import datetime
from flask_bcrypt import generate_password_hash

# Define the association table for the many-to-many relationship
user_books = db.Table('user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    biography = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Define the many-to-many relationship with Book
    books = db.relationship('Book', secondary=user_books, backref='users', lazy=True)

    def __init__(self, first_name, last_name, email, contact, user_type, password, biography, image=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.user_type = user_type
        self.password = generate_password_hash(password)  # Hash the password
        self.image = image
        self.biography = biography

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
        
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
