"""Entrance related endpoints"""

from fastapi import APIRouter, HTTPException

from ..lib.nearest_entrance import find_entrance
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
async def entrance_finder(lat: float, long: float):
    """Find nearest entrance.
    Args:
        lat: latitude of pinned point.
        long: longitude of pinned point.
    """
    try:
        res = find_entrance(lat, long)
        if not res:
            return {"msg": "No nearby entrance located for this point!"}
        else:
            print(res)
            return res

    except HTTPException as err:
        if err.detail == "something":
            raise HTTPException(status_code=400, detail="something") from err

    except Exception as err:
        LOGGER.error(
            "Unknown error happened in `find_entrance` endpoint.", exc_info=err
        )
        raise HTTPException(status_code=500) from err
