# ms-template — Agent Guide

Шаблон-репозиторий для новых микросервисов: базовый скелет FastAPI + MongoDB (Beanie ODM), из
которого через «Use this template» создаются реальные сервисы. Python 3.13, uv.

---

## Что нужно поменять при создании сервиса из шаблона

Полный чек-лист — в README.md. Коротко: имя, версия и описание в `pyproject.toml`;
`MONGO__URL`/`MONGO__DB_NAME`/`MICROSERVICES__KEY` в окружении (шаблон переменных — `.env.example`);
модели Beanie — в `document_models` внутри `initialize_database()`
(`src/core/database/registry.py`); собственные роутеры и схемы — вместо примера
`app/routers/api/hello_world.py` и `app/schemas/api/hi.py`.

---

## Commands

Используется **just** (`brew install just` / `cargo install just`):

```bash
just check         # ruff check
just fix           # ruff check --fix
just format        # ruff format
just lint          # check + format-check
just lint-fix      # fix + format
just mypy          # mypy .
just ty            # ty check .
just test          # запустить тесты (env — из .test.env)
just test-v        # тесты с подробным выводом
just test-file <file>      # запустить конкретный файл
just test-module <module>  # запустить тесты модуля (tests/<module>)
just pre-commit    # lint + ty + mypy
just fix-and-check # lint-fix + ty + mypy
just all-test       # fix-and-check + test
```

Без just — `ruff check`, `ruff format`, `mypy .`, `ty check .`, `uv sync`, `pre-commit install`
напрямую. Тестам нужен живой Mongo (`MONGO__URL`, `MONGO__DB_NAME` с суффиксом `test` —
`drop_db` в `tests/conftest.py` откажется работать с БД без него); как в CI:

```bash
docker build -f dev.Dockerfile -t localtest:latest .
docker compose -f docker-compose-test.yml run test
```

CI: `code-linting.yml` — ruff format/check + mypy + ty; `test.yml` собирает `dev.Dockerfile` и
запускает `docker compose -f docker-compose-test.yml run test`. `build-docker-image-branch.yml`
собирает и пушит образ ветки по команде `/build` в комментарии к PR, а не на каждый push —
дороже по времени, зато не тратит минуты CI на промежуточные коммиты.

---

## Архитектура

```
src/
├── main.py           # Точка входа (uvicorn)
├── app/
│   ├── app.py         # FastAPI instance с lifespan
│   ├── routers/       # API роутеры
│   ├── schemas/       # Pydantic модели запросов/ответов
│   └── depends/       # FastAPI dependencies (auth)
└── core/
    ├── settings_model.py  # Pydantic Settings
    ├── errors.py          # SuvvyError enum (fastapi-enum-errors)
    ├── database/          # Beanie ODM, registry.py
    └── logs/               # Loguru конфигурация
```

Ключевые паттерны:

- **Аутентификация**: заголовок `Microservice-Api-Key`, dependency `MicroserviceAuth`
  (`app/depends/auth.py`), навешана на всё приложение через `FastAPI(dependencies=[MicroserviceAuth])`
- **Переменные окружения**: Pydantic Settings с разделителем `__` (`MONGO__URL`, `MICROSERVICES__KEY`)
- **Ошибки**: enum `SuvvyError` с HTTP-статусами через `fastapi-enum-errors`, таблица всех ошибок
  автоматически попадает в OpenAPI через `errorenum_prepare_app` и `SuvvyError.build_md_table_for_all_errors()`

При разборе замечаний ревью — сначала попросить пользователя выбрать конкретные комментарии, не
угадывать, какие правки нужны.

---

## Тесты

- Тесты в `tests/`, структура зеркалирует `src/`, имена файлов и функций — с `test_`
- Только функции верхнего уровня, группировка в `class Test...` не используется
- Докстринг теста: `"<описание> - <ожидаемый результат>"`
- `asyncio_mode = "auto"`; `init_db`/`drop_db` в `tests/conftest.py` — автоиспользуемые фикстуры
  сессии/теста, `drop_db` откажется работать, если имя базы не оканчивается на `test`
- Тест пишется на **сценарий**, а не на строку кода: две ветки с одним наблюдаемым результатом —
  один тест

---

## Settings (env vars)

Вложенные группы через `__`, объявлены в `src/core/settings_model.py`, шаблон — `.env.example`.
Добавляя переменную — дописывать её и туда, и (если у неё нет дефолта) в `.test.env`.

| Переменная | Назначение |
|---|---|
| `MONGO__URL` | Строка подключения к MongoDB |
| `MONGO__DB_NAME` | Имя базы |
| `MONGO__CERT_FILE_PATH` | Путь к TLS-сертификату (опционально) |
| `MICROSERVICES__KEY` | Межсервисная аутентификация (`Microservice-Api-Key`) |
| `SERVER__WORKERS` | Число воркеров uvicorn, по умолчанию `1` |
