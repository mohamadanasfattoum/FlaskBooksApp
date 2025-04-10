from flask import Flask , render_template
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

@app.route('/welcome')
def index():
    # logic
    return render_template("index.html")


if __name__== "__main__":
    app.run(debug=True)