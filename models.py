from flask_sqlalchemy import SQLAlchemy # ORM for database interactions

db = SQLAlchemy()

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)

class Readers(db.Model):
    id_number = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    books_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    readers_id = db.Column(db.String, db.ForeignKey('readers.id_number'), nullable=False)
    # Relationships between models (one-to-many)
    books = db.relationship('Books', backref=db.backref('loans', cascade="all, delete-orphan"))
    readers = db.relationship('Readers', backref=db.backref('loans', cascade="all, delete-orphan"))
