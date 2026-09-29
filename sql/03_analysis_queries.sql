USE flight_analytics;

SELECT COUNT(*) AS total_flights FROM flights;
SELECT status, COUNT(*) AS flight_count FROM flights GROUP BY status ORDER BY flight_count DESC;
SELECT COUNT(*) AS delayed_flights FROM flights WHERE status='Delayed';
SELECT COUNT(*) AS cancelled_flights FROM flights WHERE status IN ('Cancelled','Canceled');
SELECT ROUND(100.0*SUM(status='Delayed')/COUNT(*),2) AS delay_percentage FROM flights;
SELECT airline_code, COUNT(*) AS flight_count FROM flights GROUP BY airline_code ORDER BY flight_count DESC;
SELECT destination_iata, COUNT(*) AS arriving_flights FROM flights GROUP BY destination_iata ORDER BY arriving_flights DESC LIMIT 10;
SELECT airport_iata, ROUND(AVG(avg_delay_min),2) AS average_delay_min FROM airport_delays GROUP BY airport_iata ORDER BY average_delay_min DESC;
SELECT a.registration,a.model,a.owner,COUNT(f.flight_id) AS flights_operated
FROM aircraft a LEFT JOIN flights f ON a.registration=f.aircraft_registration
GROUP BY a.registration,a.model,a.owner ORDER BY flights_operated DESC;
SELECT origin_iata,destination_iata,COUNT(*) AS flight_count
FROM flights GROUP BY origin_iata,destination_iata ORDER BY flight_count DESC;
SELECT DATE(scheduled_departure) AS flight_date,COUNT(*) AS total_flights,
SUM(status='Delayed') AS delayed_flights,SUM(status IN ('Cancelled','Canceled')) AS cancelled_flights
FROM flights GROUP BY DATE(scheduled_departure) ORDER BY flight_date;
