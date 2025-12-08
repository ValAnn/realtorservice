venv\Scripts\activate - активация venv
pip install -r requirements.txt

# Создайте миграции на основе моделей
python manage.py makemigrations

# Примените миграции к базе данных
python manage.py migrate

# Создайте суперпользователя для доступа к админке
python manage.py createsuperuser
# Следуйте инструкциям: введите имя пользователя, email и пароль

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте: `venv\Scripts\activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Примените миграции: `python manage.py migrate`
6. Создайте суперпользователя: `python manage.py createsuperuser`
7. Запустите сервер: `python manage.py runserver`

git rm -r --cached venv

npx cypress open


npm init -y
npm install cypress --save-dev
npx cypress open