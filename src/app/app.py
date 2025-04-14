from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_enum_errors import errorenum_prepare_app
from starlette.responses import RedirectResponse

from app.routers import router as main_router
from services.database import initialize_database
from services.errors import SuvvyError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await initialize_database()
    yield


app = FastAPI(lifespan=lifespan, description=SuvvyError.build_md_table_for_all_errors())
errorenum_prepare_app(app)


@app.get("/", include_in_schema=False)
def index_to_docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="docs")


app.include_router(main_router)
