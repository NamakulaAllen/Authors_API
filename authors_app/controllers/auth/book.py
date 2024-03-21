from flask import Blueprint, request, jsonify
from authors_app.models.book import Book
from authors_app import db

books_bp = Blueprint('books', __name__, url_prefix='/api/v1/books')

# Endpoint to create a new book
@books_bp.route('/create', methods=['POST'])
def create_book():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    pages = data.get('pages')
    price = data.get('price')
    user_id = data.get('user_id')
    company_id = data.get('company_id')

    # Create a new book object
    new_book = Book(title=title, description=description, pages=pages, price=price, user_id=user_id, company_id=company_id)

    # Add the new book to the database
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully', 'book_id': new_book.id}), 201

# Endpoint to delete a book by ID
@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 
