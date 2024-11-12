from flask import Flask, render_template, request, redirect, url_for
from models import db, Books, Readers, Loans
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable modification tracking
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/books', methods=['GET', 'POST'])
def books_manage():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        new_book = Books(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books_manage'))
    books = Books.query.all()
    return render_template('books.html', books=books)

@app.route('/readers', methods=['GET', 'POST'])
def readers_manage():
    if request.method == 'POST':
        id_number = request.form['id_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']
        new_reader = Readers(id_number=id_number, first_name=first_name, last_name=last_name, birth_date=birth_date)
        db.session.add(new_reader)
        db.session.commit()
        return redirect(url_for('readers_manage'))
    readers = Readers.query.all()
    return render_template('readers.html', readers=readers)

@app.route('/loans', methods=['GET'])
def loans_manage():
    loans = Loans.query.all()
    available_books = Books.query.filter_by(is_borrowed=False).all()
    readers = Readers.query.all()
    return render_template('loans.html', loans=loans, available_books=available_books, readers=readers)

@app.route('/loans', methods=['POST'])
def book_loan():
    book_id = request.form['book_id']
    reader_id = request.form['reader_id']
    borrow_date = date.today()
    loan = Loans(book_id=book_id, reader_id=reader_id, borrow_date=borrow_date)
    book = Books.query.get(book_id)
    book.is_borrowed = True
    db.session.add(loan)
    db.session.commit()
    return redirect(url_for('books_manage'))

@app.route('/return_book', methods=['POST'])
def book_return():
    loan_id = request.form['loan_id']
    loan = Loans.query.get(loan_id)
    loan.return_date = date.today()
    loan.book.is_borrowed = False
    db.session.commit()
    return redirect(url_for('books_manage'))

if __name__ == '__main__':
    app.run(debug=True)


