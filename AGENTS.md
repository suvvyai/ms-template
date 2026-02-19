## Язык документации

Все комментарии и docstrings пишутся на русском языке в формате rST.

## Команды разработки

Используется **just** для автоматизации команд:

```bash
just check        # ruff check
just fix          # ruff check --fix
just format       # ruff format
just lint         # check + format-check
just lint-fix     # fix + format
just mypy         # mypy .
just ty           # ty check .
just pre-commit   # lint + mypy + ty (перед коммитом)
just fix-and-check # lint-fix + mypy + ty
```

Тесты:
```bash
docker compose -f docker-compose-test.yml run test
```

## Архитектура

FastAPI микросервис с MongoDB (Beanie ODM):

```
src/
├── main.py           # Точка входа (uvicorn)
├── app/
│   ├── app.py        # FastAPI instance с lifespan
│   ├── routers/      # API роутеры
│   ├── schemas/      # Pydantic модели запросов/ответов
│   └── depends/      # FastAPI dependencies (auth)
└── core/
    ├── settings_model.py  # Pydantic Settings
    ├── errors.py          # SuvvyError enum (fastapi-enum-errors)
    ├── database/          # Beanie ODM, registry.py
    └── logs/              # Loguru конфигурация
```

## Ключевые паттерны

- **Аутентификация**: заголовок `Microservice-Api-Key`, dependency `MicroserviceAuth`
- **Переменные окружения**: Pydantic Settings с разделителем `__` (MONGO__URL, MICROSERVICES__KEY)
- **Ошибки**: enum `SuvvyError` с HTTP статусами через fastapi-enum-errors

## Конфигурация

- Python 3.13, пакетный менеджер **uv**
- Строгая типизация: mypy с `disallow_untyped_defs = true`
- ruff: line-length 120, double quotes
- pre-commit: ruff fix + format


## Стиль кода
- Документация и комментарии: на русском языке в формате reST (но без :type)
- Докстринги для тестов: "<описание теста> - <ожидаемый результат>"
- Форматирование: двойные кавычки, длина строки до 120 символов
- Типизация: обязательна ВЕЗДЕ
- Названия тестов должны начинаться с `test_`
- Структура файлов тестов должна отражать структуру проекта
- Версия Python: 3.13
- Не используй структуры типа Optional или Union. Используй более современные аналоги (через |)
- После вноски своих правок, всегда запускай `just fix-and-check`. Если ruff что-то найдет и не исправит сам, исправь ты.
