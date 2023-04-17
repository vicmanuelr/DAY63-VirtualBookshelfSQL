from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()

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

