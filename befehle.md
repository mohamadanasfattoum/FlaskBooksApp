pip install flask flask-sqlalchemy flask-migrate

source ../bin/activate

pip freeze > requirement.txt

pip install celery redis