# design models mit relations

from flask_sqlalchemy import SQLALchemy


db = SQLALchemy()


class Author(db.models):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Stringe(100),nullable=False)
    
    # ein Author hat auch books
    books = db.relationship('Book',backref='author',lazy=True)


class Book(db.models):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Stringe(100),nullable=False)

    # jedes Book hat ein Author id
    author_id = db.Column(db.Integer,db.ForeignKey('auther.id'),nullable=False)

    # ein book hat reviews
    reviews = db.relationship('Review',backref='book',lazy=True)


class Review (db.models):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text,nullable=False)

    # review hat auch book id für welches book es gehört
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'),nullable=False)