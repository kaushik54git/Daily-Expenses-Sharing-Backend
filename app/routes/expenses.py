from flask import Blueprint, request, jsonify
from app.models import mongo, Expense
from app.utils.validation import validate_expense, validate_split
from flask_jwt_extended import jwt_required
from app.utils.balance_sheet import generate_balance_sheet

bp = Blueprint('expenses', __name__)

@bp.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    errors = validate_expense(data)
    if errors:
        return jsonify(errors), 400
    if data['method'] == 'percentage':
        split_errors = validate_split(data['splits'])
        if split_errors:
            return jsonify(split_errors), 400
    expense = Expense(**data)
    mongo.db.expenses.insert_one(expense.to_dict())
    return jsonify({"message": "Expense added successfully"}), 201

@bp.route('/expenses/user/<email>', methods=['GET'])
@jwt_required()
def get_user_expenses(email):
    expenses = mongo.db.expenses.find({"splits.email": email})
    return jsonify(list(expenses)), 200

@bp.route('/expenses', methods=['GET'])
@jwt_required()
def get_all_expenses():
    expenses = mongo.db.expenses.find()
    return jsonify(list(expenses)), 200

@bp.route('/balance-sheet', methods=['GET'])
@jwt_required()
def download_balance_sheet():
    balance_sheet = generate_balance_sheet()
    response = make_response(balance_sheet)
    response.headers["Content-Disposition"] = "attachment; filename=balance_sheet.pdf"
    response.mimetype = 'application/pdf'
    return response
