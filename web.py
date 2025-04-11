from flask import Flask , render_template, request, redirect, url_for
from models import db, Book, Author, Review
from app import app

from tasks import send_book_notification

@app.route('/')
def index():
    books = Book.query.all()
    return render_template("index.html",books=books)

@app.route('/add-book',methods=['POST','GET'])
def add_book():
    
    if request.method == 'POST':
        title = request.form['title']
        author_name = request.form['author']

        # check if author with this name
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        # create Book
        book = Book(title=title,author_id=author.id)
        db.session.add(book)
        db.session.commit()

        # fire celery to send notification
        send_book_notification.delay(book.id, book.title)

        return redirect(url_for('index'))
    
    return render_template("add_book.html")

@app.route('/edit/<int:id>',methods=['POST','GET'])
def edit_book(id):
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form['title']
        author_name = request.form['author']

        # check if author with this name
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        # create Book
        book.author_id = author.id
        book.title = title
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("edit_book.html",book=book)

@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/books/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template("book_detail.html",book=book)


@app.route('/search',methods=['POST','GET'])
def search_books(): 
    if request.method == 'POST':
        query = request.form['query']
        # print(f'query: {query}') # to testing
        books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
        authors = Author.query.filter(Author.name.ilike(f'%{query}%')).all()
        return render_template("search.html",books=books,authors=authors,query=query)
    return render_template("search.html")
    
