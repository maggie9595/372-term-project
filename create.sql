DROP DATABASE IF EXISTS j9_uber;
CREATE DATABASE j9_uber;
\c j9_uber;

-- Drop dependent tables first
DROP TABLE IF EXISTS UserPaymentMethods;
DROP TABLE IF EXISTS CarOwnerships;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Rides;
DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS Riders;
DROP TABLE IF EXISTS Drivers;
DROP TABLE IF EXISTS Administrators;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS CreditCards;
DROP TABLE IF EXISTS PayPals;
DROP TABLE IF EXISTS GoogleWallets;
DROP TABLE IF EXISTS PaymentMethods;

-- Create the tables
CREATE TABLE Users (
  id           SERIAL PRIMARY KEY,
  email        TEXT NOT NULL UNIQUE,
  password     TEXT NOT NULL,
  first_name   TEXT NOT NULL,
  last_name    TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  country      TEXT NOT NULL
);

CREATE TABLE Riders (
  id      SERIAL PRIMARY KEY,
  user_id SERIAL REFERENCES Users (id)
);

CREATE TABLE Drivers (
  id                SERIAL PRIMARY KEY,
  user_id           SERIAL REFERENCES Users (id),
  current_latitude  FLOAT,
  current_longitude FLOAT,
  is_available      BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Administrators (
  id      SERIAL PRIMARY KEY,
  user_id SERIAL REFERENCES Users (id),
  title   TEXT NOT NULL
);

CREATE TABLE PaymentMethods (
  id                 SERIAL PRIMARY KEY,
  billing_first_name TEXT NOT NULL,
  billing_last_name  TEXT NOT NULL,
  billing_zipcode    TEXT NOT NULL
);

CREATE TABLE CreditCards (
  id                SERIAL PRIMARY KEY,
  payment_method_id SERIAL REFERENCES PaymentMethods (id),
  card_number       TEXT NOT NULL,
  expiration_month  INT  NOT NULL,
  expiration_year   INT  NOT NULL,
  cvv_code          TEXT NOT NULL
);

CREATE TABLE PayPals (
  id                SERIAL PRIMARY KEY,
  payment_method_id SERIAL REFERENCES PaymentMethods (id),
  paypal_email      TEXT NOT NULL,
  paypal_password   TEXT NOT NULL
);

CREATE TABLE GoogleWallets (
  id                SERIAL PRIMARY KEY,
  payment_method_id SERIAL REFERENCES PaymentMethods (id),
  login_email       TEXT NOT NULL,
  login_password    TEXT NOT NULL
);

CREATE TABLE UserPaymentMethods (
  id                      SERIAL PRIMARY KEY,
  user_id                 SERIAL REFERENCES Users (id),
  payment_method_id       SERIAL REFERENCES PaymentMethods (id),
  payment_method_nickname TEXT      NOT NULL,
  date_added              TIMESTAMP NOT NULL
);

CREATE TABLE Cars (
  id           SERIAL PRIMARY KEY,
  manufacturer TEXT NOT NULL,
  model        TEXT NOT NULL,
  year         INT  NOT NULL,
  ride_type    TEXT NOT NULL
);

CREATE TABLE CarOwnerships (
  id                  SERIAL PRIMARY KEY,
  driver_id           SERIAL REFERENCES Drivers (id),
  car_id              SERIAL REFERENCES Cars (id),
  license_plate       TEXT NOT NULL,
  car_mileage         INT  NOT NULL,
  drivers_license_num TEXT NOT NULL
);

CREATE TABLE Rides (
  id                SERIAL PRIMARY KEY,
  rider_id          SERIAL REFERENCES Riders (id),
  driver_id         SERIAL REFERENCES Drivers (id),
  start_latitude    FLOAT          NOT NULL,
  start_longitude   FLOAT          NOT NULL,
  destination       TEXT           NOT NULL,
  mileage           INT            NOT NULL,
  start_datetime    TIMESTAMP      NOT NULL,
  end_datetime      TIMESTAMP      NOT NULL,
  payment_method_id SERIAL REFERENCES PaymentMethods (id),
  price             NUMERIC(10, 2) NOT NULL,
  datetime_paid     TIMESTAMP
);
