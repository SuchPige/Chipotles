-- inform of using AI
-- chat GPT 3.5 is used for selecting proper SQL functions for executing tasks
-- code generated from AI has been debugged and modified

-- create table
CREATE TABLE chipotles (
	id SERIAL,
	state VARCHAR(50),
	location VARCHAR(50),
	address VARCHAR(255),
	latitude DOUBLE PRECISION,
	longitude DOUBLE PRECISION,
	primary key (id),
	geometry GEOMETRY(Point, 4326)
);

-- import data
COPY chipotles(state, location, address, latitude, longitude)
FROM 'D:/Documents/Study/infs7205/dataset/chipotle_stores.csv'
DELIMITER ',' CSV HEADER;

-- set geometry
UPDATE chipotles
SET geometry = ST_MakePoint(longitude, latitude);

-- task 1
SELECT *
FROM chipotles
WHERE geom && ST_MakeEnvelope(-83, 37, -80, 40, 4326);

-- task 2
SELECT *
FROM chipotles
ORDER BY ST_Distance(geom, 'SRID=4326;POINT(-70 40)') 
LIMIT 15;

-- task 3
SELECT *
FROM chipotles
WHERE ST_DWithin(
    ST_MakePoint(longitude, latitude)::geography,
    ST_MakePoint(-118, 34)::geography,
    10000
);

-- task 4
WITH polygon AS (
  SELECT ST_SetSRID(ST_GeomFromText('POLYGON((-85 39, -79 38, -81 35, -83 35, -82 38, -85 39))'), 4326) AS geom
)
SELECT *
FROM chipotles
WHERE ST_Within(geom, (SELECT geom FROM polygon));
