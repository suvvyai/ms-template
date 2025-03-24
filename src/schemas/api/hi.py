from pydantic import BaseModel


class HelloWorldRequest(BaseModel):
    name: str = "Ivan"


class HelloWorldResponse(BaseModel):
    greeting: str
