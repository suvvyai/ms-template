"""Пример роутера с эндпоинтом приветствия."""

from fastapi import APIRouter

from app.schemas.api.hi import HelloWorldRequest, HelloWorldResponse

router = APIRouter()


@router.post("/hi", description="Пример эндпоинта приветствия")
async def hello_world(body: HelloWorldRequest) -> HelloWorldResponse:
    """
    Возвращает приветствие с переданным именем.

    :param body: тело запроса с именем пользователя
    :return: ответ с приветствием
    """
    return HelloWorldResponse(greeting=f"Hello, {body.name}!")
