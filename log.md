mkdir library_project
cd library_project
mkdir backend
mkdir frontend



cd backend
python -m venv venv



venv\Scripts\activate



pip install django djangorestframework django-cors-headers djoser



django-admin startproject core .



python manage.py runserver



python manage.py startapp users
python manage.py startapp books
python manage.py startapp loans

--- 
in settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Библиотеки для API (из методички)
    'rest_framework',
    'corsheaders',
    'djoser',

    # Твои приложения
    'users',
    'books',
    'loans',
]

---

python manage.py createsuperuser

1
test@test.com
admin

---

{
    "email": "test2@test.com",
    "username": "user2",
    "password": "user2password",
    "re_password": "user2password"
}

---

admin
admin@test.com
12345