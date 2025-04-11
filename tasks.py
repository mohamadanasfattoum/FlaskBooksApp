import time
from app import celery_app


@celery_app.task
def send_book_notification(book_id,title):
    print(f"Starting notificatio task for book {book_id}:{title}")
    time.sleep(5)
    print(f"Finished sending notification for book : {book_id}")