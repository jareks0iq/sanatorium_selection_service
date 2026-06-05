- [x] Блок 0 — Аудит и подготовка
Создать ветку production-ready, пройтись по проекту, составить список того что есть и чего нет, завести IMPROVEMENT_PLAN.md с задачами.

- [x] Блок 1 — Качество кода и dev-инфраструктура
Настроить ruff (линтер + форматтер), mypy (типизация), pre-commit hooks. Проверить структуру DDD: domain → application → infrastructure → presentation. Убрать циклические импорты.

- [x] Блок 2 — Тестирование
Покрыть unit-тестами доменную логику (GP-алгоритм, бизнес-правила). Integration-тесты для репозиториев и сервисов через testcontainers. API-тесты эндпоинтов. Использовать pytest, pytest-asyncio, factory_boy, httpx, coverage. Цель: 60-70% покрытия.

- [x] Блок 3 — Документация
README.md на английском с архитектурной диаграммой (excalidraw), badges, quick start. Создать .env.example.

- [x] Блок 4 — Конфигурация и секреты
Все настройки через pydantic-settings и переменные окружения. Никаких хардкодов. Разделение конфигурации dev/test/prod. Валидация при старте приложения. 12-factor app методология.

- [ ] Блок 5 — Логирование и обработка ошибок
Структурированное логирование через structlog в JSON. Request ID middleware (correlation ID для трейсинга запросов). Свои доменные исключения. Глобальный exception handler. Маппинг доменных ошибок в HTTP-коды.

- [ ] Блок 6 — Безопасность
Хеширование паролей через bcrypt/argon2. Длинный JWT secret. Rate limiting через slowapi или Redis. Правильно настроенный CORS. Аудит валидации входных данных. Проверка на отсутствие секретов в логах.

- [ ] Блок 7 — Docker и оркестрация
Multi-stage Dockerfile (build stage + runtime stage). python:3.12-slim как база. Запуск от непривилегированного пользователя. Healthchecks. docker-compose.yml + dev/prod overrides.
-
- [ ] Блок 8 — CI/CD через GitHub Actions
CI pipeline: lint → test → security scan → build. Deployment pipeline: build → push в ghcr.io → SSH деплой на VPS → healthcheck. Семантическое версионирование.

- [ ] Блок 9 — Деплой на VPS
Купить VPS (Hetzner/Selectel/Timeweb), Ubuntu 24.04. SSH-ключи, firewall (ufw), fail2ban. Установка Docker. Купить домен. Caddy для автоматического TLS. Автоматические бэкапы PostgreSQL в S3 (Selectel/Backblaze).

- [ ] Блок 10 — Базовый мониторинг
Uptime Kuma для мониторинга доступности с алертами в Telegram. Sentry для отлова ошибок. Опционально: Prometheus + Grafana с одним дашбордом.

- [ ] Блок 11 — Финальная полировка
Нагрузочное тестирование через k6 или locust. Профилирование медленных запросов через pg_stat_statements. Добавить индексы по результатам EXPLAIN ANALYZE. Seed-скрипт make seed. Postman/Insomnia коллекция. Видео-демо.

## Отложенные улучшения (backlog)
- [ ] Блок 5: заменить все print() в handlers.py на structlog
- [ ] Блок 7: добавить PYTHONUNBUFFERED=1 и PYTHONDONTWRITEBYTECODE=1 в Dockerfile
- [ ] Обогатить базовый класс Event метаданными (occurred_at, event_id)
- [ ] Пересмотреть управление id у доменных объектов (сейчас int | None)
- [ ] UserProfile.tags меняет тип: list[int] при создании (id с сайта),
      list[Tag] при чтении из БД. Неконсистентность типов.
      Варианты: разделить create/read представления профиля, либо
      хранить только id и подгружать Tag отдельно перед recommend.
- [ ] Unit of Work
