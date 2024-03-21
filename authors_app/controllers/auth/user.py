from flask import Blueprint, request, jsonify
from authors_app.models.user import User

# Create a Blueprint for user-related routes
user_controller = Blueprint('user_controller', __name__, url_prefix='/api/v1/users')

# Endpoint to get all users
@user_controller.route('/', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'contact': user.contact,
                'user_type': user.user_type,
                'image': user.image,
                'biography': user.biography,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            user_list.append(user_data)
        
        return jsonify({'users': user_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to get a single user by ID
@user_controller.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.get_by_id(user_id)
        if user:
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'contact': user.contact,
                'user_type': user.user_type,
                'image': user.image,
                'biography': user.biography,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            return jsonify(user_data), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to update a user by ID
@user_controller.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.get_by_id(user_id)
        if user:
            data = request.json
            user.update(data)
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to delete a user by ID
@user_controller.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.get_by_id(user_id)
        if user:
            user.delete()
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
