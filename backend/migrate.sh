export $(cat .env | xargs)
python manage.py db migrate
python manage.py db upgrade
