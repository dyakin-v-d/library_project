# Library Project 📚

Полноценное Fullstack-приложение для управления библиотекой. Проект включает в себя клиентскую часть (Frontend), серверную часть (Backend) и настроенную среду развертывания через Docker.

## 🚀 Технологии

### Backend

- **Язык:** Python 3.x
- **Framework:** Django / FastAPI (выбери свой)
- **Database:** PostgreSQL (в Docker) / SQLite

### Frontend

- **Библиотека:** React / Vue (Vite)
- **Инструменты:** Axios, React Router / Vue Router

### Infrastructure

- **Контейнеризация:** Docker, Docker Compose

---

## 📁 Структура проекта

```text
library_project/
├── backend/           # Серверная логика и API
├── frontend/          # Клиентское приложение (Vite)
├── docker-compose.yml  # Конфигурация Docker
└── README.md          # Документация
```

---

## 🛠 Запуск проекта

### С использованием Docker (Рекомендуется)

Убедитесь, что у вас установлены [Docker](https://www.docker.com/) и Docker Compose.

1. **Клонируйте репозиторий:**

   ```bash
   git clone [https://github.com/dyakin-v-d/library_project.git](https://github.com/dyakin-v-d/library_project.git)
   cd library_project
   ```

2. **Запустите контейнеры:**

   ```bash
   docker-compose up --build
   ```

3. **Создайте администратора:**
   Чтобы иметь возможность войти в панель управления, выполните команду в работающем контейнере:
   ```bash
   # Для Django
   docker-compose exec backend python manage.py createsuperuser
   ```
   _Следуйте инструкциям в консоли (введите логин, email и пароль)._

---

## 🔗 Доступные адреса

После запуска проект будет доступен по следующим адресам:

- **Frontend:** [http://localhost:5173/](http://localhost:5173/) — интерфейс пользователя.
- **Админ-панель:** [http://localhost:8000/admin](http://localhost:8000/admin) — панель библиотекаря.
- **Backend API:** [http://localhost:8000/api](http://localhost:8000/api) — документация или эндпоинты.

---

## 🔧 Локальная разработка (без Docker)

### Backend

1. `cd backend`
2. `python -m venv venv`
3. `source venv/bin/activate` (или `venv\Scripts\activate` на Windows)
4. `pip install -r requirements.txt`
5. `python manage.py migrate` (для Django)
6. `python manage.py runserver`

### Frontend

1. `cd frontend`
2. `npm install`
3. `npm run dev`

---

## 👨‍💻 Автор

- **dyakin-v-d** — [GitHub Profile](https://github.com/dyakin-v-d)
