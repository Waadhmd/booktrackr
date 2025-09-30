from flask_sqlalchemy import SQLAlchemy
#db object gives you access to the db.Model class to define models, and the db.session to execute queries.
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    def __str__(self):
        birth = self.birth_date.strftime("%Y-%m-%d")
        death = self.date_of_death.strftime("%Y-%m-%d") if self.date_of_death else "Still alive"
        return f"{self.name} (Born: {birth}, Died: {death})"


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable = True)

    # Foreign key to Author
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable = False )
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f"<Book {self.id}: {self.title}"

    def __str__(self):
        year = self.publication_year if self.publication_year else 'unknown'
        return f"'{self.tite}' by {self.author.name} ({self.publication_year})"





