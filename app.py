from flask import Flask , render_template
from models import db, Book, Author, Review
app = Flask(__name__)

# configuration SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
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