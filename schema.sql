CREATE TABLE IF NOT EXISTS ride_location (
  id SERIAL PRIMARY KEY,
  latitude NUMERIC(10, 7) NOT NULL,
  longitude NUMERIC(10, 7) NOT NULL
);
CREATE TABLE IF NOT EXISTS place_meta (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  polygon GEOMETRY(POLYGON, 4326),
  entrances GEOMETRY(POINT, 4326) [] -- Array of points for entrances
);
