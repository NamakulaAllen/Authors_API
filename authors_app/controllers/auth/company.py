from flask import Blueprint, request, jsonify
from authors_app.models.company import Company  # Import the Company model
from flask_bcrypt import generate_password_hash
from authors_app import db

company = Blueprint('company', __name__, url_prefix='/api/v1/company')

@company.route('/register', methods=['POST'])
def register():
    try:
        name = request.json.get('name')
        industry = request.json.get('industry')
        location = request.json.get('location')
        user_id = request.json.get('user_id')

        # Input validation
        if not name or not industry or not location:
            return jsonify({"error": "All fields are required"}), 400

        # Create a new company instance
        new_company = Company(name=name, industry=industry, location=location)

        # Adding and committing to the database
        db.session.add(new_company)
        db.session.commit()

        return jsonify({
            'message': f'Company {new_company.name} has been successfully registered.',
            'company': {
                'name': new_company.name,
                'industry': new_company.industry,
                'location': new_company.location,
                'created_at': new_company.created_at,
                'user_id': new_company.user_id,
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
