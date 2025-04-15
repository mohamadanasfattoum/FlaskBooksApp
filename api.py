from flask import jsonify
from app import app , db

from models import Book, Author , Review

# schema for book  to convert book to json
def book_list_to_dict(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author.name 
    }

def book_detail_to_dict(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author.name,
        'reviews': [{'id':review.id , 'content':review.content} for review in book.reviews]
    }
# 
@app.route('/api/books', methods=['GET'])
def books_list_api():
    books = Book.query.all()
    return jsonify({
        'books': [book_list_to_dict(book) for book in books]
    })
  
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book_api(id):
    # book = Book.query.filter_by(id=id).first()
    book = Book.query.get_or_404(id)
    return jsonify(book_detail_to_dict(book))



@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book_api(id):
    book = Book.query.get_or_404(id)
    return jsonify({'message': 'Book updated successfully'})



@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book_api(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})


@app.route('/api/books', methods=['POST'])
def create_book_api():
    pass
 