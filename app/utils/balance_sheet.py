from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.models import mongo

def generate_balance_sheet():
    c = canvas.Canvas("balance_sheet.pdf", pagesize=letter)
    width, height = letter

    users = mongo.db.users.find()
    expenses = mongo.db.expenses.find()

    y = height - 30
    c.drawString(30, y, "Balance Sheet")
    y -= 30

    for user in users:
        c.drawString(30, y, f"User: {user['name']} ({user['email']})")
        y -= 20
        user_expenses = mongo.db.expenses.find({"splits.email": user['email']})
        for expense in user_expenses:
            c.drawString(50, y, f"Expense: {expense['description']} - {expense['amount']}")
            y -= 20

    c.save()
    with open("balance_sheet.pdf", "rb") as f:
        return f.read()
