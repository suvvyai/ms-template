"""Модуль обработчиков логирования."""

import inspect
import logging

from loguru import logger


class UvicornHandler(logging.Handler):
    """
    Обработчик для перенаправления логов Uvicorn в Loguru.

    Позволяет использовать единый формат логирования через Loguru
    для всех логов приложения, включая логи Uvicorn.
    """

    def emit(self, record: logging.LogRecord) -> None:
        """
        Обрабатывает запись лога и перенаправляет её в Loguru.

        :param record: запись лога из стандартного модуля logging
        """
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        if record.name == "uvicorn.access":
            level = "REQUEST"

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
