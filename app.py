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
# Now initialize the db with the app
db.init_app(app)

@app.route('/add_author',methods=['GET','POST'])
def add_author():
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
    authors = Author.query.all()
    return render_template('authors.html', authors=authors)

#with app.app_context():
 #   db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
