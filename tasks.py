import time
from app import celery_app

# Celery task to send a notification for a book
@celery_app.task
def send_book_notification(book_id, title):
    # Simulate sending a notification with a delay
    print(f"Starting notification task for book {book_id}: {title}")
    time.sleep(5)  # Simulate a delay (e.g., sending an email or push notification)
    print(f"Finished sending notification for book: {book_id}")