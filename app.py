from flask import Flask , render_template, request, redirect, url_for
import os
from models import db, Book, Author, Review
app = Flask(__name__)

# Configuration for SQLAlchemy - database will be created in current folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'books.db')}"
# app.config[''] = '' 

# initialize the app with the extension
db.init_app(app)

# generate tables
with app.app_context():
    db.create_all()

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

if __name__== "__main__":
    app.run(debug=True)