from flask import Flask, render_template, request, redirect, url_for
from models import db, Books, Readers, Loans
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
db.init_app(app)

with app.app_context():
    db.create_all()

# Add template context processor for current year (for Footer on base.html)
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Main page
@app.route('/')
def index():
    return render_template('welcome.html')

# Books management page
@app.route('/books', methods=['GET', 'POST'])
def books_manage():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        # create a new book
        new_book = Books(title=title, author=author)
        # add the book to the database
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books_manage'))

    # display data in ascending order
    books = Books.query.order_by(Books.title.asc()).all()

    # create a list with book and loan info
    books_with_loans = []
    for book in books:
        loan_info = None
        if book.is_borrowed:
            loan_info = Loans.query.filter_by(books_id=book.id, return_date=None).first()  # Get current active loan
        books_with_loans.append((book, loan_info))
    
    return render_template('books.html', books_with_loans=books_with_loans)

# Delete book
@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Books.query.get_or_404(book_id)
    
    # Check if the book is not borrowed
    if book.is_borrowed:
        return "Cannot delete book: Book is currently borrowed", 400
    
    # If book is not borrowed, proceed with deletion
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books_manage'))

# Readers management page
@app.route('/readers', methods=['GET', 'POST'])
def readers_manage():
    if request.method == 'POST':
        id_number = request.form['id_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date_str = request.form['birth_date']
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        # create a new reader
        new_reader = Readers(id_number=id_number, first_name=first_name, last_name=last_name, birth_date=birth_date)

        # add the reader to the database
        db.session.add(new_reader)
        db.session.commit()
        return redirect(url_for('readers_manage'))
    
    # display data in ascending order
    readers = Readers.query.order_by(Readers.first_name.asc()).all()
    
    # Get active loans for each reader
    readers_with_loans = []
    for reader in readers:
        has_active_loans = Loans.query.filter_by(readers_id=reader.id_number, return_date=None).first() is not None
        readers_with_loans.append((reader, has_active_loans))
    
    return render_template('readers.html', readers_with_loans=readers_with_loans)

# Delete reader
@app.route('/delete_reader/<string:reader_id>', methods=['POST'])
def delete_reader(reader_id):
    reader = Readers.query.filter_by(id_number=reader_id).first()
    
    # Check if reader has any active loans
    active_loans = Loans.query.filter_by(readers_id=reader.id_number, return_date=None).first()
    if active_loans:
        return "Cannot delete reader: Reader has borrowed books that haven't been returned", 400
    
    # If reader has no active loans, proceed with deletion
    db.session.delete(reader)
    db.session.commit()
    return redirect(url_for('readers_manage'))

# Loans management page
@app.route('/loans', methods=['GET', 'POST'])
def loans_manage():
    if request.method == 'POST':
        books_id = request.form['books_id']
        readers_id = request.form['readers_id']
        borrow_date = date.today()

        # create a new loan
        loan = Loans(books_id=books_id, readers_id=readers_id, borrow_date=borrow_date)

        # update the book's is_borrowed status
        book = Books.query.get(books_id)
        book.is_borrowed = True

        # add the loan to the database
        db.session.add(loan)
        db.session.commit()
        return redirect(url_for('loans_manage'))
    
    loans = Loans.query.all()
    available_books = Books.query.filter_by(is_borrowed=False).all()
    readers = Readers.query.all()
    return render_template('loans.html', loans=loans, available_books=available_books, readers=readers)

# Return book
@app.route('/return_book', methods=['POST'])
def book_return():
    loan_id = request.form['loan_id']
    loan = Loans.query.get(loan_id)
    loan.return_date = date.today()

    # update the book's is_borrowed status
    loan.books.is_borrowed = False
    db.session.commit()
    return redirect(url_for('loans_manage'))

# Delete loan
@app.route('/delete_loan/<int:loan_id>', methods=['POST'])
def delete_loan(loan_id):
    loan = Loans.query.get_or_404(loan_id)
    
    # Check if the book is returned
    if not loan.return_date:
        return "Cannot delete loan: Book hasn't been returned yet", 400
    
    # If book is returned, proceed with deletion
    db.session.delete(loan)
    db.session.commit()
    return redirect(url_for('loans_manage'))

if __name__ == '__main__':
    app.run(debug=True)
