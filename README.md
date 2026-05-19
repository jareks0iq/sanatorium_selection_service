# 🏥 Сервис выбора санатория методом целевого программирования

Веб-сервис для подбора санатория, максимально соответствующего предпочтениям пользователя. Ранжирование выполняется алгоритмом **Weighted Goal Programming** — методом многокритериальной оптимизации.

Курсовая работа, СПбГЭТУ «ЛЭТИ», кафедра ИС, 2026.

---

## Возможности

- Регистрация и аутентификация пользователей
- Профиль с настройкой предпочтений: бюджет, регион, цель отдыха, медицинский профиль, услуги, условия проживания
- Система тегов (28 тегов в 3 категориях) для описания санаториев и предпочтений пользователя
- Слайдеры приоритетов — пользователь задаёт важность каждого критерия
- Алгоритм Weighted Goal Programming для ранжирования санаториев
- Каталог санаториев с детальным просмотром
- Сравнение до 3 санаториев бок о бок
- Система отзывов с рейтингом
- Смена пароля

---

## Стек технологий

| Слой | Технология |
|------|-----------|
| Backend | Python, Flask, SQLAlchemy 2.0 |
| Frontend | React (JavaScript) |
| БД | PostgreSQL |
| Контейнеризация | Docker, docker-compose |

---

## Архитектура

Проект построен по принципам **Domain-Driven Design** (по книге Персиваля «Architecture Patterns with Python»):

```
courseSanat/
├── domain/                  # Доменный слой
│   ├── model.py             # Сущности: User, UserProfile, Sanatorium, Tag, Review
│   └── goal_programming.py  # Алгоритм Weighted Goal Programming
├── adapters/                # Инфраструктурный слой
│   ├── database.py          # Подключение к БД, промежуточные таблицы
│   ├── orm.py               # ORM-маппинг (SQLAlchemy)
│   └── repository.py        # Репозитории (паттерн Repository)
├── service_layer/           # Сервисный слой
│   ├── services.py          # Бизнес-логика
│   ├── handlers.py          # Обработчики событий
│   └── MessageBus.py        # Шина событий (Event Bus)
├── entrypoints/             # Точки входа
│   └── flask_app.py         # REST API (Flask)
├── frontend/                # React-приложение
│   └── src/App.js           # Единый компонент с навигацией
├── seed.py                  # Наполнение БД тестовыми данными
├── Dockerfile               # Сборка бэкенда
├── docker-compose.yml       # Оркестрация всех сервисов
└── requirements.txt         # Python-зависимости
```

### Используемые паттерны

**Domain-Driven Design** — доменные модели не зависят от БД и фреймворков. Бизнес-логика инкапсулирована в домене.

**Repository Pattern** — репозитории абстрагируют доступ к данным. Домен работает с чистыми Python-объектами, конвертация в ORM происходит в репозиториях.

**Service Layer** — координирует вызовы между доменом и репозиториями, обрабатывает транзакции.

**Event-Driven Architecture** — доменные объекты генерируют события (UserRegistered, ProfileCreated, ReviewCreated), шина событий маршрутизирует их в обработчики.

**Data Mapper** — ORM-классы отделены от доменных моделей, маппинг выполняется в слое репозиториев.

---

## Алгоритм Weighted Goal Programming

Метод целевого программирования решает задачу многокритериальной оптимизации: пользователь имеет несколько целей одновременно (дёшево, в нужном регионе, с нужными услугами), и алгоритм находит вариант с минимальным суммарным отклонением от всех целей.

### Формализация

Для каждого санатория вычисляется **score** — взвешенная сумма нормализованных отклонений от целей пользователя. Чем меньше score — тем лучше санаторий соответствует запросу.

#### Шаг 1: Нормализация весов

Пользователь задаёт приоритеты критериев (от 1 до 10). Веса нормализуются:

```
w_i = priority_i / (priority_budget + priority_region + priority_medical + priority_services + priority_conditions)
```

Сумма всех w_i = 1.

#### Шаг 2: Вычисление отклонений

**Бюджет** (percentage normalization):
```
d_budget = max(0, budget_санатория - budget_цель) / budget_цель
```
Если санаторий дешевле цели — отклонение = 0 (это не проблема). Если дороже — отклонение пропорционально превышению.

**Регион** (бинарное):
```
d_region = 0, если регион совпал
d_region = 1, если регион не совпал
```

**Теги по категориям** (доля несовпадения):
```
d_medical = 1 - |выбранные_medical ∩ теги_санатория_medical| / |выбранные_medical|
d_services = 1 - |выбранные_services ∩ теги_санатория_services| / |выбранные_services|
d_conditions = 1 - |выбранные_conditions ∩ теги_санатория_conditions| / |выбранные_conditions|
```
Если пользователь не выбрал тегов в категории — отклонение = 0.

#### Шаг 3: Итоговый score

```
score = w_budget * d_budget + w_region * d_region + w_medical * d_medical + w_services * d_services + w_conditions * d_conditions
```

Все отклонения находятся в диапазоне [0, 1], что позволяет складывать их без искажений. Санатории сортируются по возрастанию score.

---

## Запуск

### С Docker (рекомендуется)

```bash
git clone https://github.com/jareks0iq/sanatorium_selection_service.git
cd sanatorium_selection_service
docker-compose up --build
```

После запуска:
- Фронтенд: http://localhost:3000
- API: http://localhost:5000
- БД заполняется автоматически через seed

### Без Docker

**Требования:** Python 3.11+, Node.js 18+, PostgreSQL 15+

1. Создайте БД `sanat` в PostgreSQL

2. Бэкенд:
```bash
pip install -r requirements.txt
python seed.py
python entrypoints/flask_app.py
```

3. Фронтенд:
```bash
cd frontend
npm install
npm start
```

---

## API endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| GET | /api/tags | Все теги |
| GET | /api/sanatoriums/ | Все санатории |
| GET | /api/sanatoriums/\<id\> | Санаторий по ID |
| POST | /api/register | Регистрация |
| POST | /api/login | Вход |
| POST | /api/profile | Создание/обновление профиля |
| PUT | /api/password | Смена пароля |
| POST | /api/recommend | Получение рекомендаций (Weighted GP) |
| GET | /api/reviews/\<sanatorium_id\> | Отзывы санатория |
| POST | /api/reviews | Создание отзыва |

---

## Структура БД

**users** — пользователи (id, name, login, password)

**profiles** — профили с предпочтениями и весами критериев

**sanatoriums** — санатории (name, budget, region, food, rating)

**tags** — теги трёх категорий: medical, services, conditions

**sanatorium_tags** — связь many-to-many между санаториями и тегами

**profile_tags** — связь many-to-many между профилями и тегами

**reviews** — отзывы (user_id, sanatorium_id, text, rating, created_at)

---

## Автор

Студент СПбГЭТУ «ЛЭТИ», кафедра ИС, группа 4374, 2026
