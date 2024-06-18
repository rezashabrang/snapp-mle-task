"""Schema definition for `http_entrance` endpoints"""

from typing import List
from pydantic import BaseModel


class PolygonPayload(BaseModel):
    """Polygon payload for finding entrances"""

    coordinates: List[List[float]]

    model_config = {
        "json_schema_extra": {
            "example": {
                "coordinates": [
                    [51.41681851494866, 35.65187874692117],
                    [51.41744830103832, 35.64760059502382],
                    [51.42087064573448, 35.64719545756819],
                    [51.421273776391985, 35.64733883570075],
                    [51.42128511578716, 35.65056043270057],
                    [51.41681851494866, 35.65187874692117],
                ]
            }
        }
    }
