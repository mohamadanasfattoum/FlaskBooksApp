pip install flask flask-sqlalchemy flask-migrate

source ../bin/activate

pip freeze > requirement.txt

pip install celery redis


# to run celery
celery -A app.celery_app  worker --loglevel INFO

# to redis 

sudo apt install redis-server
sudo systemctl start redis
sudo systemctl status redis 