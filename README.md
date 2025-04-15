# FlaskBooksApp

FlaskBooksApp is a Flask-based application that provides a REST API and web interface for managing books, authors, and reviews. It also integrates Celery for background task processing.

## Project Structure

```
FlaskBooksApp/
├── src/
│   ├── app.py          # Main Flask application and Celery initialization
│   ├── api.py          # API routes for managing books
│   ├── models.py       # Database models for Book, Author, and Review
│   ├── tasks.py        # Celery tasks for background processing
│   ├── web.py          # Web routes for the user interface
│   └── templates/      # HTML templates for the web interface
├── migrations/         # Database migration files
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Features

- **RESTful API**: Manage books, authors, and reviews via JSON-based endpoints.
- **Web Interface**: User-friendly interface for managing books and authors.
- **Celery Integration**: Perform background tasks such as notifications.
- **SQLite Database**: Store and manage data locally.
- **Modular Design**: Separate files for API, tasks, models, and web routes.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/FlaskBooksApp.git
   cd FlaskBooksApp
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db upgrade
   ```

5. Start the Redis server (required for Celery):
   ```bash
   redis-server
   ```

6. Run the Celery worker:
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

7. Run the Flask application:
   ```bash
   flask run
   ```

## Web Routes

### Homepage

- **GET** `/`: Displays a list of all books.

### Add Book

- **GET/POST** `/add-book`: Add a new book with an associated author.

### Edit Book

- **GET/POST** `/edit/<id>`: Edit the details of an existing book.

### Delete Book

- **GET** `/delete/<id>`: Delete a book by its ID.

### Book Details

- **GET** `/books/<id>`: View details of a specific book.

### Search

- **GET/POST** `/search`: Search for books and authors by title or name.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

