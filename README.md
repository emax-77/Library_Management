***the project is under construction - eta 13.11.2024***

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

1. Vytvorenie databázy (model databázy sa nachádza v súbore models.py) nasledovne:

- tabuľka Knihy 

    - book_id (Primary Key)
    - title (Text)
    - author (Text)
    - is_borrowed (Boolean)

- tabuľka Čitatelia

    - id_number (Primary Key)
    - first_name (Text)
    - last_name (Text)
    - birth_date (Date)

- tabuľka Výpožičky

    - loan_id (Primary Key)
    - borrow_date (Date)
    - return_date (Date)
    - book_id (Foreign Key na tabulku Knihy)
    - reader_id (Foreign Key na tabulku Čitatelia)

2. Vytvorenie routingov a views v main.py

3. Vytvorenie frontendovej časti
    - HTML súbory sa nachádzajú v adresári templates
    - CSS sa nachádza v adresári static







