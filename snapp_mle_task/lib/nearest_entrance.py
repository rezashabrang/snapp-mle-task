"""Funtionalities for finding nearest entrance"""

from typing import List, Optional

import re

from .db import PostgresSingletonConn

# Regular expression pattern to match coordinates
PATTERN = r"POINT\(([-+]?\d*\.\d+) ([-+]?\d*\.\d+)\)"


def find_entrance(lat: float, long: float) -> Optional[List[float]]:
    """Wrapper function for finding nearet entrance.
    Args:
        lat: latitude of given point.
        long: longitude of given point.

    Returns:
        Coordinates for the entrance or None if there is no nearby entrance.
    """
    poly_exist_res = check_existence_in_polygon(lat, long)
    # There is no polygon that encompasses that point
    if not poly_exist_res:
        return None

    return find_nearest_entrance(lat, long, poly_exist_res[0])


def check_existence_in_polygon(lat: float, long: float):
    """Function for checking if a point exists in already defined polygons"""

    conn = PostgresSingletonConn()
    cursor = conn.cursor()
    # Be vary of sql injection :)
    query = f"""
        SELECT id, name
        FROM place_meta
        WHERE ST_Contains(polygon, ST_GeomFromText('POINT({long} {lat})', 4326));
    """
    cursor.execute(query)
    res = cursor.fetchone()
    cursor.close()
    return res


def find_nearest_entrance(long: float, lat: float, poly_id: int) -> List[float]:
    """Find nearest entrance.
    Args:
        lat: latitude of given point.
        long: longitude of given point.
        poly_id: The id of the polygon in database

    Retuns:
        Coordinates for the nearest entrance.
    """
    conn = PostgresSingletonConn()
    cursor = conn.cursor()
    # Be vary of sql injection :)
    query = f"""
        SELECT
            nearest_entrance
        FROM
            place_meta,
            LATERAL (
                SELECT
                    ST_AsText(entrance) AS nearest_entrance,
                    ST_DistanceSpheroid(entrance, ST_GeomFromText('POINT({long} {lat})', 4326)) AS distance
                FROM
                    unnest(entrances) AS entrance
                WHERE id={poly_id}
                ORDER BY
                    distance
                LIMIT 1
            ) AS subquery
        ORDER BY distance;
    """
    cursor.execute(query)
    res = cursor.fetchone()
    # Use re.search to find the coordinates in the string
    match = re.search(PATTERN, res[0])
    # Extract coordinates from the matched groups
    longitude = float(match.group(1))
    latitude = float(match.group(2))
    cursor.close()
    return [latitude, longitude]
