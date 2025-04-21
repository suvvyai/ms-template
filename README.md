# Репозиторий-шаблон для микросервисов внутри Савви

[![Использовать этот шаблон](https://img.shields.io/badge/Использовать_этот_шаблон-blue?style=for-the-badge&logoColor=white&logo=github)](https://github.com/suvvyai/ms-template/generate)

## Содержание шаблона

Данный шаблон содержит базовую структуру микросервиса для быстрого старта разработки:

### Основная структура

- **FastAPI приложение**:
  - Маршрутизаторы в `src/app/routers`
  - Модели Pydantic в `src/schemas` и `src/models`
  - Пример API эндпоинта в `src/app/routers/api/hello_world.py`

- **MongoDB интеграция**:
  - Подключение через Beanie ORM
  - Инициализация базы данных в `src/services/database.py`

- **Конфигурация**:
  - Настройки через переменные окружения в `src/services/settings_model.py`
  - Логирование через Loguru в `src/services/logs/handlers.py`
  - Обработка ошибок в `src/services/errors.py`
  - Аутентификация микросервисов в `src/services/auth.py`

- **Докеризация**:
  - `Dockerfile` для продакшена
  - `dev.Dockerfile` для разработки
  - `docker-compose.yml` для запуска сервиса
  - `docker-compose-test.yml` для запуска тестов

- **Инструменты разработки**:
  - **Python 3.13**
  - **uv** для управления зависимостями
  - **pytest** для тестирования
  - **ruff** для линтинга и форматирования
  - **mypy** для проверки типов
  - **pre-commit** для авто-использования **ruff**

## Что нужно изменить для использования

1. **Настройки проекта**:
   - Обновить имя и описание проекта в `pyproject.toml`

2. **Настройки базы данных**:
   - Настроить MongoDB URL, имя БД и путь к сертификату в переменных окружения
   - Добавить модели документов Beanie в `initialize_database()` в `src/services/database.py`

3. **Аутентификация**:
   - Настроить API ключи микросервисов в переменных окружения

4. **Разработка API**:
   - Создать необходимые маршрутизаторы в `src/app/routers`
   - Добавить модели схем в `src/schemas`
   - Реализовать бизнес-логику в `src/services`

## Переменные окружения

```env
MONGO__URL=mongodb://user:password@mongodb:27017
MONGO__DB_NAME=your_db_name
MONGO__CERT_FILE_PATH=/path/to/cert.pem (опционально)

MICROSERVICES__KEY=your-secret-key
```

## Список основных команд

```bash
ruff check
ruff format
mypy .
pre-commit install
uv sync
```
