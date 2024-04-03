from flask import Blueprint, request, jsonify
from authors_app.extensions import db, bcrypt
from authors_app.models.user import User
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Route for user registration
@auth.route('/register',  methods=['POST'])
def register():
    try: 
        # Extract data from JSON request
        first_name = request.json['first_name'] 
        last_name = request.json['last_name']
        email = request.json['email']
        contact = request.json['contact']
        password = request.json['password']
        user_type = request.json['user_type']
        image = request.json['image']
        biography = request.json['biography']  # Include biography field
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Validate input data
        if not first_name:
            return jsonify({"error":"Your first name is required"}), 400
        if not last_name:
            return jsonify({"error":"Your last name is required"}), 400
        if not email:
            return jsonify({"error":"Your email is required"}), 400
        if not contact:
            return jsonify({"error":"Your contact is required"}), 400
        if not user_type:
            return jsonify({"error":"User type is required"}), 400
        if len(password) < 6:
            return jsonify({"error":"Your password must have more than six characters"}), 400
        
        # Check if email and contact are unique
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "This email is already registered"}), 400
        if User.query.filter_by(contact=contact).first():
            return jsonify({"error": "This contact is already registered"}), 400
        
        # Create a new user object
        new_user = User(first_name=first_name, last_name=last_name, email=email,
                        contact=contact, password=hashed_password, user_type=user_type, image=image,
                        biography=biography)  # Include biography field

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route for user login
@auth.route('/login', methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            user_password = bcrypt.check_password_hash(user.password, password)
            if user_password:
                access_token = create_access_token(identity=user.id)
                return jsonify({
                    'user': {
                        'id': user.id,
                        'username': user.get_full_name(),
                        'email': user.email,
                        'access_token': access_token,
                    }
                }), 200
            else:
                return jsonify({'error': "Invalid password"}), 401

        return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for editing user information
@auth.route('/edit/<int:user_id>', methods=["PUT"])
def edit_user(user_id):
    try:
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            new_email = data['email']
            if new_email != user.email and User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'The email already exists'}), 400
            user.email = new_email
        if 'image' in data:
            user.image = data['image']
        if 'biography' in data:
            user.biography = data['biography']
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'password' in data:
            password = data['password']
            if len(password) < 6:
                return jsonify({'error': 'Password must have at least 6 characters'}), 400
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        if 'contact' in data:
            user.contact = data['contact']

        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500    

# Route for deleting user
@auth.route('/delete/<int:user_id>', methods=["DELETE"])
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
