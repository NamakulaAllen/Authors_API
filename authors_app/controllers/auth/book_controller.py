from flask import Blueprint, request, jsonify
from authors_app.extensions import db
from authors_app.models.book import Book
from datetime import datetime

book = Blueprint('book', __name__, url_prefix='/api/v1/book')

@book.route('/register', methods=['POST'])
def register_book():
    try:
        # Extracting request data
        title = request.json.get('title')
        description = request.json.get('description')
        price = request.json.get('price')
        image = request.json.get('image')
        number_of_pages = request.json.get('number_of_pages')
        user_id = request.json.get('user_id')

        # Basic input validation
        if not title:
            return jsonify({"error": 'Your book title is required'}), 400

        if not user_id:
            return jsonify({"error": 'Your book user_id is required'}), 400

        if not description:
            return jsonify({"error": 'The description is required'}), 400

        if not image:
            return jsonify({"error": 'The image is required'}), 400

        if not number_of_pages:
            return jsonify({"error": 'The number_of_pages is required'}), 400

        if not price:
            return jsonify({"error": 'The price is required'}), 400

        # Creating a new book instance
        new_book = Book(
            title=title,
            description=description,
            price=price,
            number_of_pages=number_of_pages,
            image=image,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Adding the new book to the database
        db.session.add(new_book)
        db.session.commit()

        # Building a response message
        return jsonify({"message": f"Book '{new_book.title}' with ID '{new_book.id}' has been registered successfully."}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
