USE flight_analytics;

-- Change C:/FlightAnalytics/data/ to your actual CSV folder.
LOAD DATA LOCAL INFILE 'C:/FlightAnalytics/data/airport.csv'
INTO TABLE airport
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/FlightAnalytics/data/aircraft.csv'
INTO TABLE aircraft
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/FlightAnalytics/data/airport_delays.csv'
INTO TABLE airport_delays
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/FlightAnalytics/data/flights.csv'
INTO TABLE flights
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 ROWS;

SELECT 'airport' AS table_name, COUNT(*) AS row_count FROM airport
UNION ALL SELECT 'aircraft', COUNT(*) FROM aircraft
UNION ALL SELECT 'airport_delays', COUNT(*) FROM airport_delays
UNION ALL SELECT 'flights', COUNT(*) FROM flights;
