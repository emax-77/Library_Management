# Library Management Web app using Flask and SQLite 

## Requirements
- Python 
- Flask
- Flask-SQLAlchemy
 
 ## Installation
 - Clone the repository:
 - Install the required dependencies:
 ```pip install -r requirements.txt```
 - Run main.py

## Postup pri vytvorení aplikácie

1. Vytvorenie databázy by malo byť nasledovné:

- Tabulka Knihy 

    - book_id (Primary Key)
    - title (Text)
    - author (Text)
    - is_borrowed (Boolean)

- Tabulka Čitatelia

    - id_number (Primary Key)
    - first_name (Text)
    - last_name (Text)
    - birth_date (Date)

- Tabulka Výpožičky

    - loan_id (Primary Key)
    - borrow_date (Date)
    - return_date (Date)
    - book_id (Foreign Key na tabulku Knihy)
    - reader_id (Foreign Key na tabulku Čitatelia)

2. Vytvorenie modelov
    - modely nachádzajú v adresári models.py







