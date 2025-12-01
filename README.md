venv\Scripts\activate - активация venv
pip install -r requirements.txt

# Создайте миграции на основе моделей
python manage.py makemigrations

# Примените миграции к базе данных
python manage.py migrate

# Создайте суперпользователя для доступа к админке
python manage.py createsuperuser
# Следуйте инструкциям: введите имя пользователя, email и пароль