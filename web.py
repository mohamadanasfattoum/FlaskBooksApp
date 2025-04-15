from flask import Flask, render_template, request, redirect, url_for
from models import db, Book, Author, Review
from app import app
from tasks import send_book_notification

# Route to display the homepage with a list of all books
@app.route('/')
def index():
    books = Book.query.all()  # Fetch all books from the database
    return render_template("index.html", books=books)

# Route to add a new book
@app.route('/add-book', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']  # Get book title from form
        author_name = request.form['author']  # Get author name from form

        # Check if an author with this name exists, otherwise create a new author
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        # Create a new book and associate it with the author
        book = Book(title=title, author_id=author.id)
        db.session.add(book)
        db.session.commit()

        # Trigger a Celery task to send a notification
        send_book_notification.delay(book.id, book.title)

        return redirect(url_for('index'))  # Redirect to the homepage

    return render_template("add_book.html")  # Render the add book form

# Route to edit an existing book
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit_book(id):
    book = Book.query.get_or_404(id)  # Fetch the book or return 404 if not found

    if request.method == 'POST':
        title = request.form['title']  # Get updated title from form
        author_name = request.form['author']  # Get updated author name from form

        # Check if an author with this name exists, otherwise create a new author
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        # Update the book's title and author
        book.author_id = author.id
        book.title = title
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to the homepage

    return render_template("edit_book.html", book=book)  # Render the edit book form

# Route to delete a book
@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)  # Fetch the book or return 404 if not found
    db.session.delete(book)  # Delete the book from the database
    db.session.commit()
    return redirect(url_for('index'))  # Redirect to the homepage

# Route to display details of a specific book
@app.route('/books/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)  # Fetch the book or return 404 if not found
    return render_template("book_detail.html", book=book)  # Render the book details page

# Route to search for books and authors
@app.route('/search', methods=['POST', 'GET'])
def search_books():
    if request.method == 'POST':
        query = request.form['query']  # Get the search query from the form
        # Search for books and authors matching the query
        books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
        authors = Author.query.filter(Author.name.ilike(f'%{query}%')).all()
        return render_template("search.html", books=books, authors=authors, query=query)
    return render_template("search.html")  # Render the search form

