CREATE DATABASE IF NOT EXISTS flight_analytics;
USE flight_analytics;

DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS airport_delays;
DROP TABLE IF EXISTS aircraft;
DROP TABLE IF EXISTS airport;

CREATE TABLE airport (
    airport_id INT PRIMARY KEY,
    icao_code VARCHAR(10) NOT NULL UNIQUE,
    iata_code CHAR(3) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    city VARCHAR(80),
    state VARCHAR(80),
    country VARCHAR(80),
    continent VARCHAR(40),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    timezone VARCHAR(60),
    airport_type VARCHAR(30)
);

CREATE TABLE aircraft (
    aircraft_id INT PRIMARY KEY,
    registration VARCHAR(20) NOT NULL UNIQUE,
    model VARCHAR(60),
    manufacturer VARCHAR(60),
    icao_type_code VARCHAR(10),
    owner VARCHAR(80)
);

CREATE TABLE airport_delays (
    delay_id INT PRIMARY KEY,
    airport_iata CHAR(3) NOT NULL,
    delay_date DATE NOT NULL,
    total_flights INT,
    delayed_flights INT,
    avg_delay_min DECIMAL(10,2),
    median_delay_min DECIMAL(10,2),
    canceled_flights INT,
    CONSTRAINT fk_delay_airport FOREIGN KEY (airport_iata) REFERENCES airport(iata_code)
);

CREATE TABLE flights (
    flight_id VARCHAR(30) PRIMARY KEY,
    flight_number VARCHAR(20) NOT NULL,
    aircraft_registration VARCHAR(20),
    origin_iata CHAR(3) NOT NULL,
    destination_iata CHAR(3) NOT NULL,
    scheduled_departure DATETIME,
    actual_departure DATETIME,
    scheduled_arrival DATETIME,
    actual_arrival DATETIME,
    status VARCHAR(30) NOT NULL,
    airline_code VARCHAR(10),
    CONSTRAINT fk_flight_aircraft FOREIGN KEY (aircraft_registration) REFERENCES aircraft(registration),
    CONSTRAINT fk_flight_origin FOREIGN KEY (origin_iata) REFERENCES airport(iata_code),
    CONSTRAINT fk_flight_destination FOREIGN KEY (destination_iata) REFERENCES airport(iata_code)
);
