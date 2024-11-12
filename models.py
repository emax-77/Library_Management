from flask_sqlalchemy import SQLAlchemy # ORM for database interactions

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)

class Reader(db.Model):
    id_number = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    reader_id = db.Column(db.String, db.ForeignKey('reader.id_number'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    # Relationships
    book = db.relationship('Book', backref=db.backref('loans', cascade="all, delete-orphan"))
    reader = db.relationship('Reader', backref=db.backref('loans', cascade="all, delete-orphan"))
