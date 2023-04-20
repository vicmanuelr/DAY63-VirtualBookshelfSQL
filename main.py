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


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    db = SQLAlchemy()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
    db.init_app(app)
    return app, db


app, db = create_app()


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

