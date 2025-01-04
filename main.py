from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import io
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    mobile = db.Column(db.String(20), unique=True, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    total_amount = db.Column(db.Float, nullable=False)
    split_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class ExpenseParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float)
    percentage = db.Column(db.Float)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    mobile = data.get('mobile')
    if not email or not name or not mobile:
        return jsonify({'error': 'Invalid input'}), 400
    user = User(email=email, name=name, mobile=mobile)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'User already exists'}), 400
    return jsonify({'message': 'User created', 'user_id': user.id}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'email': user.email, 'name': user.name, 'mobile': user.mobile})

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    description = data.get('description')
    total_amount = data.get('total_amount')
    split_method = data.get('split_method')
    participants = data.get('participants')
    if not total_amount or not split_method or not participants:
        return jsonify({'error': 'Invalid input'}), 400
    
    expense = Expense(description=description, total_amount=total_amount, split_method=split_method)
    db.session.add(expense)
    db.session.commit()
    
    total_percentage = 0
    for participant in participants:
        user_id = participant.get('user_id')
        amount = participant.get('amount')
        percentage = participant.get('percentage')
        if split_method == 'percentage':
            total_percentage += percentage
        expense_participant = ExpenseParticipant(expense_id=expense.id, user_id=user_id, amount=amount, percentage=percentage)
        db.session.add(expense_participant)
    if split_method == 'percentage' and total_percentage != 100:
        return jsonify({'error': 'Percentages do not add up to 100'}), 400
    db.session.commit()
    
    return jsonify({'message': 'Expense added', 'expense_id': expense.id}), 201

@app.route('/expenses/user/<int:user_id>', methods=['GET'])
def get_user_expenses(user_id):
    expenses = Expense.query.join(ExpenseParticipant).filter(ExpenseParticipant.user_id == user_id).all()
    return jsonify([{'id': e.id, 'description': e.description, 'total_amount': e.total_amount, 'split_method': e.split_method} for e in expenses])

@app.route('/expenses', methods=['GET'])
def get_overall_expenses():
    expenses = Expense.query.all()
    return jsonify([{'id': e.id, 'description': e.description, 'total_amount': e.total_amount, 'split_method': e.split_method} for e in expenses])

@app.route('/balancesheet/download', methods=['GET'])
def download_balance_sheet():
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['User ID', 'Name', 'Email', 'Total Amount', 'Split Method', 'Description'])
    users = User.query.all()
    for user in users:
        expenses = Expense.query.join(ExpenseParticipant).filter(ExpenseParticipant.user_id == user.id).all()
        for expense in expenses:
            writer.writerow([user.id, user.name, user.email, expense.total_amount, expense.split_method, expense.description])
    buffer.seek(0)
    return send_file(io.BytesIO(buffer.getvalue().encode()), mimetype='text/csv', attachment_filename='balance_sheet.csv', as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
