from authors_app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    image = db.Column(db.BLOB, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship with users
    user = db.relationship('User', backref='book_user', lazy=True)  # Singular name for relationship

    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)  # Optional company

    # Relationship with companies (if needed)
    company = db.relationship('Company', backref='books')  # Singular name for relationship (if used)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, title, description, pages, price, user_id, company_id=None):
        self.title = title
        self.description = description
        self.pages = pages
        self.price = price
        self.user_id = user_id
        self.company_id = company_id

    def __repr__(self):
        return f'Book({self.title})'
