from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy

# import sqlite3
#
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# # cursor.execute("CREATE TABLE books ("
# #                "id INTEGER PRIMARY KEY,"
# #                "title varchar(250) NOT NULL UNIQUE,"
# #                "author varchar(250) NOT NULL,"
# #                "rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

SECRET_KEY = '1234567890'

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'SECRET_KEY'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.name}>'


with app.app_context():
    db.create_all()
    new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)

with app.app_context():
    db.session.commit()
    Book.query.all()

class AddBook(FlaskForm):
    book_name = StringField(label='Book Name', validators=[DataRequired()])
    book_author = StringField(label='Book Author', validators=[DataRequired()])
    book_rating = IntegerField(label='Book Rating', validators=[NumberRange(min=0, max=10)])
    submit = SubmitField('Add Book')


all_books = []


@app.route('/')
def home():
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddBook()
    if form.validate_on_submit():
        new_entry = dict(title=form.book_name.data, author=form.book_author.data, rating=form.book_rating.data)
        all_books.append(new_entry)
        print(all_books)
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

