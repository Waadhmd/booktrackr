# 📚 Flask Library App

A simple library management application built with **Flask** and **SQLAlchemy**.  
You can add authors and books, search and sort them, view book details, and delete books (and optionally their authors).

---

##  Features
- Add authors with birth/death dates
- Add books with title, ISBN, publication year, and author
- Search books by title or author
- Sort books by title or author
- View book details
- Delete books (and delete the author too if they have no more books)
- Flash messages for success feedback

---
## Install dependencies
pip install -r requirements.txt

## Initialize the database
from app import app, db
with app.app_context():
    db.create_all()