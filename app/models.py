from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def init_app(app: Flask):
    mongo.init_app(app)

# User Model
class User:
    def __init__(self, email, name, mobile):
        self.email = email
        self.name = name
        self.mobile = mobile

    def to_dict(self):
        return {
            "email": self.email,
            "name": self.name,
            "mobile": self.mobile
        }

# Expense Model
class Expense:
    def __init__(self, description, amount, method, splits):
        self.description = description
        self.amount = amount
        self.method = method
        self.splits = splits

    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "method": self.method,
            "splits": self.splits
        }
