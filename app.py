from flask import Flask 
from models import db
from celery import Celery, Task
import os

# Initialize the Flask application
app = Flask(__name__)

# Function to initialize Celery with Flask app context
def celery_init_app(app: Flask) -> Celery:
    # Custom Celery Task class to use Flask app context
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs) 

    # Create and configure the Celery app
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])  # Load Celery config from Flask app
    celery_app.set_default()  # Set this Celery app as the default
    app.extensions["celery"] = celery_app  # Attach Celery to Flask app extensions
    return celery_app

# Flask app configuration for Celery
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",  # Redis as the message broker
        result_backend="redis://localhost",  # Redis as the result backend
        task_ignore_result=True,  # Ignore task results to save resources
    ),
)
celery_app = celery_init_app(app)  # Initialize Celery with the Flask app

# Configuration for SQLAlchemy - database will be created in the current folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'books.db')}"  # SQLite database

# Initialize the app with the SQLAlchemy extension
db.init_app(app)

# Generate database tables if they don't exist
with app.app_context():
    db.create_all()

# Import routes and tasks
from web import *  # Import web routes
from tasks import send_book_notification  # Import Celery task
from api import *  # Import API routes

# Run the Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)