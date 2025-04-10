# design models

from flask_sqlalchemy import SQLALchemy


db = SQLALchemy()


class Author(db.models):
    pass




class Book(db.models):
    pass


class Review (db.models):
    pass