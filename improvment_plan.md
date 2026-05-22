Неделя 1 (20–26 мая)
Блок 0 — Аудит и подготовка (1-2 вечера)
Создать ветку production-ready, пройтись по проекту, составить список того что есть и чего нет, завести IMPROVEMENT_PLAN.md с задачами.

Блок 1 — Качество кода и dev-инфраструктура (3-5 вечеров)
Настроить ruff (линтер + форматтер), mypy (типизация), pre-commit hooks. Проверить структуру DDD: domain → application → infrastructure → presentation. Убрать циклические импорты.
Неделя 2 (27 мая — 2 июня)

Блок 2 — Тестирование (5-7 вечеров)
Покрыть unit-тестами доменную логику (GP-алгоритм, бизнес-правила). Integration-тесты для репозиториев и сервисов через testcontainers. API-тесты эндпоинтов. Использовать pytest, pytest-asyncio, factory_boy, httpx, coverage. Цель: 60-70% покрытия.
Неделя 3 (3–9 июня)

Блок 3 — Документация (2-3 вечера)
README.md на английском с архитектурной диаграммой (excalidraw), badges, quick start. Создать docs/architecture.md, docs/api.md, папку docs/adr/ с Architecture Decision Records. CHANGELOG.md, CONTRIBUTING.md, .env.example.

Блок 4 — Конфигурация и секреты (2 вечера)
Все настройки через pydantic-settings и переменные окружения. Никаких хардкодов. Разделение конфигурации dev/test/prod. Валидация при старте приложения. 12-factor app методология.
Неделя 4 (10–16 июня)

Блок 5 — Логирование и обработка ошибок (3 вечера)
Структурированное логирование через structlog в JSON. Request ID middleware (correlation ID для трейсинга запросов). Свои доменные исключения. Глобальный exception handler. Маппинг доменных ошибок в HTTP-коды.

Блок 6 — Безопасность (2-3 вечера)
Хеширование паролей через bcrypt/argon2. Длинный JWT secret. Rate limiting через slowapi или Redis. Правильно настроенный CORS. Аудит валидации входных данных. Проверка на отсутствие секретов в логах.
Неделя 5 (17–23 июня)

Блок 7 — Docker и оркестрация (3 вечера)
Multi-stage Dockerfile (build stage + runtime stage). python:3.12-slim как база. Запуск от непривилегированного пользователя. Healthchecks. docker-compose.yml + dev/prod overrides.
Блок 8 — CI/CD через GitHub Actions (3-4 вечера)
CI pipeline: lint → test → security scan → build. Deployment pipeline: build → push в ghcr.io → SSH деплой на VPS → healthcheck. Семантическое версионирование.
Неделя 6 (24–30 июня)

Блок 9 — Деплой на VPS (3-4 вечера)
Купить VPS (Hetzner/Selectel/Timeweb), Ubuntu 24.04. SSH-ключи, firewall (ufw), fail2ban. Установка Docker. Купить домен. Caddy для автоматического TLS. Автоматические бэкапы PostgreSQL в S3 (Selectel/Backblaze).

Блок 10 — Базовый мониторинг (2-3 вечера)
Uptime Kuma для мониторинга доступности с алертами в Telegram. Sentry для отлова ошибок. Опционально: Prometheus + Grafana с одним дашбордом.

Блок 11 — Финальная полировка (2-3 вечера)
Нагрузочное тестирование через k6 или locust. Профилирование медленных запросов через pg_stat_statements. Добавить индексы по результатам EXPLAIN ANALYZE. Seed-скрипт make seed. Postman/Insomnia коллекция. Видео-демо.