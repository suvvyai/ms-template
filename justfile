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

# === Комбинированные команды ===

# Проверить всё перед коммитом (lint + mypy + ty)
pre-commit: lint mypy ty

# Исправить и проверить
fix-and-check: lint-fix mypy ty