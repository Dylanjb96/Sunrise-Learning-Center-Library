from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    transactions = db.relationship('Transaction', backref='book', lazy=True)

    def is_available(self):
        return self.available > 0

    def borrow(self):
        if self.is_available():
            self.available -= 1
            return True
        return False

    def return_book(self):
        self.available += 1

class Member(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    borrowed = db.Column(db.Integer, nullable=False, default=0)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    transactions = db.relationship('Transaction', backref='member', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('member.member_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    employee_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    hash = db.Column(db.Text, nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    deleted = db.Column(db.Integer, nullable=False, default=0)