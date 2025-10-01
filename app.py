from sqlalchemy import asc
from sqlalchemy.orm import joinedload

from data_models import db, Author, Book
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

# Needed for flash()
app.secret_key = "supersecretkey123"
# initialize the db with the app
db.init_app(app)

@app.route('/add_author',methods=['GET','POST'])
def add_author():
    """
     Route: /add_author
     - GET: Render a form to add a new author.
     - POST: Validate form input, add author to database,
       then redirect to authors list with a flash success message.
     """
    success = None
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        birth_date_str = data.get('birth_date')
        date_of_death_str = data.get('date_of_death')

        try:
            birth_date = datetime.strptime(birth_date_str,"%Y-%m-%d").date()
        except Exception:
            birth_date = None

        # Parse optional death date
        date_of_death = None
        if date_of_death_str:
            try:
                date_of_death = datetime.strptime(date_of_death_str, "%Y-%m-%d").date()
            except Exception:
                date_of_death = None

        if name and birth_date:
            author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
            db.session.add(author)
            db.session.commit()
            flash(f"Author '{name}' added successfully!", "success")
            return redirect(url_for('list_authors'))

    return render_template('add_author.html',success = success)

@app.route('/authors')
def list_authors():
    """
    Route: /authors
    - Lists all authors currently stored in the database.
    """
    authors = Author.query.all()
    return render_template('authors.html', authors=authors)

@app.route('/add_book',methods=['GET','POST'])
def add_book():
    """
     Route: /add_book
     - GET: Show a form to add a new book (with dropdown for authors).
     - POST: Add a new book to the database if valid input is provided.
     """
    authors = Author.query.all()
    success = None
    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year_str = request.form.get('publication_year')
        author_id = request.form.get('author_id')
        publication_year = None
        if publication_year_str:
            try:
                publication_year = int(publication_year_str)
            except ValueError:
                publication_year = None

        if title and isbn and author_id:
            book = Book(
                title=title,
                isbn=isbn,
                publication_year=publication_year,
                author_id=int(author_id),
            )
            db.session.add(book)
            db.session.commit()
            success = f"Book {title} added successfully."

    return render_template('add_book.html',authors=authors,success=success)

@app.route('/',methods=['GET'])
def home():
    """
    Route: /
    - Displays all books with optional sorting and search functionality.
    - Sorting: by title (default) or author.
    - Searching: matches query against book title or author name
    """
    sort_by = request.args.get('sort', 'title')
    search_query = request.args.get('q','')

    query = Book.query.options(joinedload(Book.author))
    #if search term provided
    if search_query:
        query = query.join(Author).filter(
            (Book.title.ilike(f"%{search_query}%")) |
            (Author.name.ilike(f"%{search_query}%"))
        )

    if sort_by == 'author':
        query = query.join(Author).order_by(asc(Author.name))
    else:
        query = query.order_by(asc(Book.title))
    books = query.all()

    return render_template('home.html', books=books, sort_by=sort_by, search_query=search_query)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """
      Route: /book/<book_id>
      - Shows detailed information about a specific book.
      - Returns 404 if book does not exist.
      """
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/book/<int:book_id>/delete',methods=['POST'])
def delete_book(book_id):
    """
    Route: /book/<book_id>/delete
    - Deletes the selected book.
    - If the book's author has no remaining books, deletes the author too.
    - Redirects to homepage with a flash success message.
    """
    book = Book.query.get_or_404(book_id)

    author = book.author
    # Delete the book
    db.session.delete(book)
    db.session.commit()
    # If the author has no more books, delete them too
    if not author.books:
        db.session.delete(author)
        db.session.commit()
        flash(f"Book '{book.title}' and author '{author.name}' were deleted successfully.", "success")
    else:
        flash(f"Book '{book.title}' was deleted successfully.", "success")

    return redirect(url_for('home'))



 #with app.app_context():
 #   db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
