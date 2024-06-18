"""Fast API Main Configuration"""

from typing import Union

import os

from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi

from snapp_mle_task.lib.db import init_database
from snapp_mle_task.routers import http_entrance

# Initialize postgres
init_database()

app = FastAPI()


DESCRIPTION = """
Entry Locator API
"""


async def get_token_header(x_token: str = Header(...)) -> Union[None, Exception]:
    """."""
    if x_token != os.getenv("API_KEY"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return None


def custom_openapi():
    """Defining custom API schema."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Entry Locator API",
        version="0.1",
        description=DESCRIPTION,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore

app.include_router(
    http_entrance.router,
    prefix=os.getenv("ROOT_PATH", ""),
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
