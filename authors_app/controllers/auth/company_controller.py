from flask import Blueprint, request, jsonify
from authors_app.extensions import db
from authors_app.models import Company
from datetime import datetime

company = Blueprint('company', __name__, url_prefix='/api/v1/company')

@company.route('/register', methods=['POST'])
def register_company():
    try:
        # Extracting request data
        id = request.json.get('id')
        name = request.json.get('name')
        origin = request.json.get('origin')
        description = request.json.get('description')
        
        # Basic input validation
        if not id:
            return jsonify({"error": 'Your company ID is required'}), 400

        if not name:
            return jsonify({"error": 'Your company name is required'}), 400

        if not origin:
            return jsonify({"error": 'Your company origin is required'}), 400

        if not description:
            return jsonify({"error": 'Please add a description of your company'}), 400

        # Creating a new company
        new_company = Company(
            id=id,
            name=name,
            origin=origin,
            description=description,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Add the company to the database
        db.session.add(new_company)
        db.session.commit()

        # Building a response message
        message = f"Company {new_company.name} has been registered successfully."
        return jsonify({"message": message}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
