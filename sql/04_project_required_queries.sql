USE flight_analytics;

-- =========================================================
-- FLIGHT ANALYTICS PROJECT
-- 11 REQUIRED ANALYSIS QUERIES
-- =========================================================


-- =========================================================
-- QUERY 1
-- Total flights per aircraft model
-- =========================================================

SELECT
    a.model AS aircraft_model,
    COUNT(f.flight_id) AS total_flights
FROM aircraft a
JOIN flights f
    ON f.aircraft_registration = a.registration
GROUP BY a.model
ORDER BY total_flights DESC;


-- =========================================================
-- QUERY 2
-- Aircraft assigned to more than 5 flights
-- =========================================================

SELECT
    a.registration,
    a.model,
    COUNT(f.flight_id) AS flight_count
FROM aircraft a
JOIN flights f
    ON f.aircraft_registration = a.registration
GROUP BY
    a.registration,
    a.model
HAVING COUNT(f.flight_id) > 5
ORDER BY flight_count DESC;


-- =========================================================
-- QUERY 3
-- Airports with more than 5 outbound flights
-- =========================================================

SELECT
    a.iata_code,
    a.name AS airport_name,
    COUNT(f.flight_id) AS outbound_flights
FROM airport a
JOIN flights f
    ON f.origin_iata = a.iata_code
GROUP BY
    a.iata_code,
    a.name
HAVING COUNT(f.flight_id) > 5
ORDER BY outbound_flights DESC;


-- =========================================================
-- QUERY 4
-- Top 3 destination airports by arriving flights
-- =========================================================

SELECT
    a.iata_code,
    a.name AS airport_name,
    a.city,
    COUNT(f.flight_id) AS arriving_flights
FROM airport a
JOIN flights f
    ON f.destination_iata = a.iata_code
GROUP BY
    a.iata_code,
    a.name,
    a.city
ORDER BY arriving_flights DESC
LIMIT 3;


-- =========================================================
-- QUERY 5
-- Domestic vs International flights
-- =========================================================

SELECT
    f.flight_number,
    origin.name AS origin_airport,
    destination.name AS destination_airport,
    CASE
        WHEN origin.country = destination.country
            THEN 'Domestic'
        ELSE 'International'
    END AS flight_type
FROM flights f
JOIN airport origin
    ON f.origin_iata = origin.iata_code
JOIN airport destination
    ON f.destination_iata = destination.iata_code
ORDER BY f.flight_number;


-- =========================================================
-- QUERY 6
-- Five most recent arrivals at DEL
-- =========================================================

SELECT
    f.flight_number,
    f.aircraft_registration AS aircraft,
    origin.name AS departure_airport,
    f.actual_arrival AS arrival_time
FROM flights f
JOIN airport origin
    ON f.origin_iata = origin.iata_code
WHERE f.destination_iata = 'DEL'
  AND f.actual_arrival IS NOT NULL
ORDER BY f.actual_arrival DESC
LIMIT 5;


-- =========================================================
-- QUERY 7
-- Airports with no arriving flights
-- =========================================================

SELECT
    a.iata_code,
    a.name AS airport_name,
    a.city
FROM airport a
LEFT JOIN flights f
    ON f.destination_iata = a.iata_code
WHERE f.flight_id IS NULL
ORDER BY a.name;


-- =========================================================
-- QUERY 8
-- Airline flight counts by status
-- =========================================================

SELECT
    airline_code,
    SUM(
        CASE
            WHEN status = 'Landed' THEN 1
            ELSE 0
        END
    ) AS landed_count,

    SUM(
        CASE
            WHEN status = 'Delayed' THEN 1
            ELSE 0
        END
    ) AS delayed_count,

    SUM(
        CASE
            WHEN status IN ('Canceled', 'Cancelled') THEN 1
            ELSE 0
        END
    ) AS cancelled_count,

    SUM(
        CASE
            WHEN status = 'Scheduled' THEN 1
            ELSE 0
        END
    ) AS scheduled_count,

    SUM(
        CASE
            WHEN status = 'Departed' THEN 1
            ELSE 0
        END
    ) AS departed_count,

    COUNT(*) AS total_flights

FROM flights
GROUP BY airline_code
ORDER BY total_flights DESC;


-- =========================================================
-- QUERY 9
-- Cancelled flights with aircraft and airports
-- =========================================================

SELECT
    f.flight_number,
    f.aircraft_registration AS aircraft,
    origin.name AS origin_airport,
    destination.name AS destination_airport,
    f.scheduled_departure
FROM flights f
JOIN airport origin
    ON f.origin_iata = origin.iata_code
JOIN airport destination
    ON f.destination_iata = destination.iata_code
WHERE f.status IN ('Canceled', 'Cancelled')
ORDER BY f.scheduled_departure DESC;


-- =========================================================
-- QUERY 10
-- City pairs with more than 2 aircraft models
-- =========================================================

SELECT
    origin.city AS origin_city,
    destination.city AS destination_city,
    COUNT(DISTINCT a.model) AS aircraft_model_count
FROM flights f
JOIN airport origin
    ON f.origin_iata = origin.iata_code
JOIN airport destination
    ON f.destination_iata = destination.iata_code
JOIN aircraft a
    ON f.aircraft_registration = a.registration
GROUP BY
    origin.city,
    destination.city
HAVING COUNT(DISTINCT a.model) > 2
ORDER BY
    aircraft_model_count DESC,
    origin.city,
    destination.city;


-- =========================================================
-- QUERY 11
-- Destination airport delay percentage
-- =========================================================

SELECT
    a.iata_code,
    a.name AS airport_name,
    COUNT(f.flight_id) AS total_arrivals,

    SUM(
        CASE
            WHEN f.status = 'Delayed' THEN 1
            ELSE 0
        END
    ) AS delayed_arrivals,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN f.status = 'Delayed' THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(f.flight_id), 0),
        2
    ) AS delayed_percentage

FROM airport a
JOIN flights f
    ON f.destination_iata = a.iata_code
GROUP BY
    a.iata_code,
    a.name
ORDER BY delayed_percentage DESC;