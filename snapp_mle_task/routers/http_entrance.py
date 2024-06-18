"""Entrance related endpoints"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from ..lib.schema.entrance import PolygonPayload
from ..logger import LOGGER

# ------------------------------ Initialization -------------------------------
router = APIRouter()


# ---------------------------- Routers ----------------------------
@router.get(
    "/",
    status_code=200,
)
async def main():
    """main entry point."""
    return {"msg": "Welcome to Entry Locator API!"}


@router.get(
    "/find-nearest-entrance",
    status_code=200,
)
async def find_entrance(lat: float, long: float):
    """Find nearest entrance.
    Args:
        lat: latitude of pinned point.
        long: longitude of pinned point.
    """
    try:
        return {}

    except HTTPException as err:
        if err.detail == "something":
            raise HTTPException(status_code=400, detail="something") from err

    except Exception as err:
        LOGGER.error(
            "Unknown error happened in `find_entrance` endpoint.", exc_info=err
        )
        raise HTTPException(status_code=500) from err


@router.post(
    "/identify-entrances",
    status_code=200,
)
async def identify_entrances(polygon_payload: PolygonPayload):
    """Identify the entrancs for a given polygon.
    Note that for coordinates must be in format [{longitude}, {latitude}]
    """
    try:
        return {}

    except HTTPException as err:
        if err.detail == "something":
            LOGGER.error(f"Some log message!")
            return JSONResponse(status_code=404, content={"msg": "some-error"})

    except Exception as err:
        LOGGER.error(
            "Unknown error happened in `identify_entrances` endpoint.", exc_info=err
        )
        raise HTTPException(status_code=500) from err
