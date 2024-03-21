from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from authors_app.models.user import User
from authors_app import db

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.route('/register', methods=['POST'])
def register():
    try:
        # Extract request data
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        contact = data.get('contact')
        user_type = data.get('user_type')
        password = data.get('password')
        biography = data.get('biography', '')
        image = data.get('image')

        # Input validation
        if not all([first_name, last_name, email, contact, user_type, password, image]):
            return jsonify({"error": "All fields are required"}), 400
        
        if len(password) < 8:
            return jsonify({"error": "Password should have 8 or more characters"}), 400

        if user_type == 'author' and not biography:
            return jsonify({"error": "Biography is required for authors"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400

        if User.query.filter_by(contact=contact).first():
            return jsonify({"error": "Contact already exists"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create the user
        new_user = User(first_name=first_name, last_name=last_name, email=email, contact=contact,
                        password=hashed_password, user_type=user_type, biography=biography, image=image)
        
        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Build the response
        username = new_user.get_full_name()
        response_data = {
            'message': f'{username} has been successfully created as an {new_user.user_type}',
            'user': {
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'contact': new_user.contact,
                'type': new_user.user_type,
                'created_at': new_user.created_at,
            }
        }
        return jsonify(response_data), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Endpoint to delete a user
@auth.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Endpoint to update a user
@auth.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.json
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.contact = data.get('contact', user.contact)
        user.user_type = data.get('user_type', user.user_type)
        user.biography = data.get('biography', user.biography)
        user.image = data.get('image', user.image)

        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
