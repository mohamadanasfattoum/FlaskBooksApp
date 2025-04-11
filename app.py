from flask import Flask 
from models import db
from celery import Celery, Task
import os


app = Flask(__name__)

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs) 

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)


# Configuration for SQLAlchemy - database will be created in current folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'books.db')}"
# app.config[''] = '' 

# initialize the app with the extension
db.init_app(app)

# generate tables
with app.app_context():
    db.create_all()

from web import *
from tasks import send_book_notification 

if __name__== "__main__":
    app.run(debug=True)