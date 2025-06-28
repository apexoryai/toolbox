-- DDL: Database schema for Hotel Management Toolbox

-- Table: hotel_tier
CREATE TABLE IF NOT EXISTS hotel_tier (
    id SERIAL PRIMARY KEY,
    tier_name VARCHAR(32) UNIQUE NOT NULL,
    cost INTEGER
);

-- Table: hotels
CREATE TABLE IF NOT EXISTS hotels(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    hotel_tier_id INTEGER REFERENCES hotel_tier(id)
);

-- Table: bookings
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    checkin_date DATE NOT NULL,
    checkout_date DATE NOT NULL
); 