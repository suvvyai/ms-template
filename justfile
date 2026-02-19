# Justfile для автоматизации команд разработки
# Установка: brew install just (macOS) или cargo install just

# Показать список доступных команд
default:
    @just --list

# === Линтинг и форматирование ===

# Запустить ruff check
check:
    ruff check .

# Запустить ruff check с автоисправлением
fix:
    ruff check --fix .

# Отформатировать код
format:
    ruff format .

# Проверить форматирование без изменений
format-check:
    ruff format --check .

# Запустить все проверки линтера (check + format-check)
lint: check format-check

# Исправить все проблемы линтера (fix + format)
lint-fix: fix format

# === Проверка типов ===

# Запустить mypy
mypy:
    mypy .

# Запустить ty (проверка типов от Astral)
ty:
    ty check .

# === Тесты ===

# Переменные
test_env := ".test.env"
test_local_env := ".test.local.env"

# Загрузить переменные окружения для тестов
[private]
load-test-env:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ ! -f "{{test_local_env}}" ]]; then
        echo "Ошибка: файл {{test_local_env}} не найден"
        echo "Создайте его на основе {{test_env}}"
        exit 1
    fi

# Запустить все тесты
test *args:
    #!/usr/bin/env bash
    set -a
    source {{test_env}}
    source {{test_local_env}}
    set +a
    python -m pytest {{args}}

# Запустить тесты с подробным выводом
test-v *args:
    just test -v --no-header {{args}}

# Запустить конкретный тестовый файл
test-file file *args:
    just test-v {{file}} {{args}}

# Запустить тесты для определённого модуля (например: just test-module test_app)
test-module module *args:
    just test-v tests/{{module}} {{args}}

# === Комбинированные команды ===

# Проверить всё перед коммитом (lint + mypy + ty)
pre-commit: lint mypy ty

# Исправить и проверить
fix-and-check: lint-fix mypy ty

# Исправить и проверить
all: fix-and-check

# Исправить и проверить + тесты
all-test: fix-and-check test
