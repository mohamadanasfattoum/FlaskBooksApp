from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy for database operations
db = SQLAlchemy()

# Author model: Represents an author in the database
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Author's name (required)

    # One-to-many relationship: An author can have multiple books
    books = db.relationship('Book', backref='author', lazy=True)

# Book model: Represents a book in the database
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(100), nullable=False)  # Book title (required)

    # Foreign key: Each book is associated with one author
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    # One-to-many relationship: A book can have multiple reviews
    reviews = db.relationship('Review', backref='book', lazy=True)

# Review model: Represents a review for a book
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    content = db.Column(db.Text, nullable=False)  # Review content (required)

    # Foreign key: Each review is associated with one book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)