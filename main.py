from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Books, Readers, Loans
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('base.html')