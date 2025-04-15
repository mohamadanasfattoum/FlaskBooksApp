from flask import jsonify, request
from app import app, db
from models import Book, Author, Review

# Helper function to convert a book object to a dictionary for JSON response
def book_list_to_dict(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author.name  # Accessing the author's name
    }

# Helper function to include detailed book information, including reviews
def book_detail_to_dict(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author.name,
        'reviews': [{'id': review.id, 'content': review.content} for review in book.reviews]
    }

# API endpoint to fetch a list of all books
@app.route('/api/books', methods=['GET'])
def books_list_api():
    books = Book.query.all()  # Fetch all books from the database
    return jsonify({
        'books': [book_list_to_dict(book) for book in books]  # Convert books to JSON
    })

# API endpoint to fetch details of a specific book by ID
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book_api(id):
    book = Book.query.get_or_404(id)  # Fetch book or return 404 if not found
    return jsonify(book_detail_to_dict(book))

# API endpoint to update a book's details
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book_api(id):
    book = Book.query.get_or_404(id)  # Fetch book or return 404 if not found
    data = request.get_json()  # Parse JSON payload

    # Update book attributes if provided in the request
    title = data.get('title')
    author_id = data.get('author_id')
    author = data.get('author')

    if title:
        book.title = title
    if author:
        book.author.name = author
    if author_id:
        book.author_id = author_id

    db.session.commit()  # Save changes to the database
    return jsonify(book_detail_to_dict(book))

# API endpoint to delete a book by ID
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book_api(id):
    book = Book.query.get_or_404(id)  # Fetch book or return 404 if not found
    db.session.delete(book)  # Delete the book from the database
    db.session.commit()  # Commit the transaction
    return jsonify({'message': 'Book deleted successfully'})

# API endpoint to create a new book
@app.route('/api/books', methods=['POST'])
def create_book_api():
    data = request.get_json()  # Parse JSON payload

    # Validate required fields
    title = data.get('title')
    author_id = data.get('author_id')

    if not title or not author_id:
        return jsonify({'error': 'Title and author_id are required'}), 400

    # Create and save the new book
    book = Book(title=title, author_id=author_id)
    db.session.add(book)
    db.session.commit()

    # Return the updated list of books
    books = Book.query.all()
    return jsonify({
        'books': [book_list_to_dict(book) for book in books]
    })
