# NutriLog

Персональный дневник питания с анализом КБЖУ.

## Возможности системы

- регистрация и авторизация пользователей;
- ведение дневника питания: добавление, редактирование и удаление записей по датам;
- автоматический расчёт индивидуальной нормы КБЖУ по формуле Миффлина–Сан Жеора;
- просмотр текущего профиля и нормы потребления;
- недельная статистика питания.

## Используемые технологии

**Бэкенд**
- Python
- FastAPI
- PostgreSQL
- Redis

**Фронтенд**
- Vue

**Дополнительно**
- Docker / Docker Compose
- Git, GitHub
- Render

## Запуск через Docker

```bash
git clone https://github.com/AnnaGS05/nutrition-diary.git
cd nutrition-diary

docker-compose up --build
```

После запуска:
- Фронтенд: http://localhost
- Бекенд API: http://localhost:8000
- Документация API (Swagger): http://localhost:8000/docs

## REST API

POST   /auth/register   Регистрация пользователя
POST   /auth/login   Вход в систему
POST   /auth/logout   Выход из системы
GET   /auth/me   Проверка текущей авторизации

GET   /api/entries/   Список записей питания за дату
POST   /api/entries/   Создание записи питания
PUT   /api/entries/{id}   Обновление записи питания
DELETE   /api/entries/{id}   Удаление записи питания

GET   /api/profile/   Получение профиля пользователя
POST   /api/profile/   Сохранение профиля и расчёт нормы КБЖУ

GET   /api/stats   Статистика КБЖУ за день
GET   /api/stats/weekly   Статистика КБЖУ за неделю

GET   /health   Проверка работоспособности сервера
GET   /instance   Идентификатор текущего контейнера

## Тестирование

В проекте реализовано property-based фаззинг-тестирование с использованием
библиотеки `hypothesis`. Тесты автоматически генерируют случайные входные
данные и проверяют, что сервер корректно отклоняет невалидные значения и
никогда не возвращает ошибку 500.

```bash
cd backend/app/tests
pip install -r requirements-test.txt
python -m pytest fuzz_test.py -v
```

Перед запуском тестов бекенд должен быть запущен.

## Развёртывание

Проект развёрнут на платформе Render. Инфраструктура включает четыре сервиса: бекенд, фронтенд,
PostgreSQL и Redis.

Приложение доступно по адресу:
**https://nutrilog-frontend.onrender.com**

## Автор

Головина Анна Сергеевна, ИКБО-12-23
