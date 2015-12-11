\c j9_uber

--- SIMPLE QUERIES ---

\echo -- 1. As a driver, I want to sign up with my car.
\echo -- First creating a user account for the driver.
INSERT INTO Users (email, password, first_name, last_name, phone_number, country)
VALUES ('maggie@gmail.com', 'password', 'Maggie', 'Yu', '717-000-0000', 'US');

\echo
\echo -- Creating a driver account and attaching it to the generic user account.
INSERT INTO Drivers (user_id, is_available, current_latitude, current_longitude)
VALUES ((SELECT MAX(id) FROM Users), true, 79.9764, 40.4397);

\echo
\echo -- Registering the drivers car with by adding a new Car Ownership record.
INSERT INTO CarOwnerships (driver_id, car_id, license_plate, car_mileage, drivers_license_num)
VALUES ((SELECT MAX(id) FROM Drivers), 3, '14D AA8', 26042, 'A1032-1243-5783');

\echo
\echo -- 2. As an admin, I want to add a new type of car listing into Uber.
\echo -- Adding a new car to the Cars table (which lists the permitted cars on Uber)
INSERT INTO Cars (manufacturer, model, year, ride_type)
VALUES ('Honda', 'Civic', 2014, 'X');

\echo
\echo -- 3. As a rider, I want to sign up.
\echo -- First creating a user account for the rider.
INSERT INTO Users (email, password, first_name, last_name, phone_number, country)
VALUES ('jimmyfallon@gmail.com', 'iloveponies', 'Jimmy', 'Fallon', '610-429-0811', 'US');

\echo
\echo -- Creating a rider account and attaching it to the generic user account.
INSERT INTO Riders (user_id, current_latitude, current_longitude)
VALUES ((SELECT MAX(id) FROM Riders), 179.9764, 140.4397);

\echo
\echo -- 4. As a driver, I want to set myself as available to give rides.
UPDATE Drivers 
SET is_available = true
WHERE id = 2;

\echo
\echo -- 5. As an admin, I want to view ride history on a particular day.
SELECT *
FROM Rides
WHERE start_datetime BETWEEN '2015-02-04 00:00:00' AND '2015-02-04 23:59:59';

\echo
\echo -- 6. As an admin, I want to view the list of all available drivers in the U.S.
SELECT *
FROM Drivers as d
INNER JOIN Users as u
ON d.user_id = u.id
WHERE (d.is_available = true) AND (u.country = 'US');

\echo
\echo -- 7. As a rider, I want to link my PayPal account to my Uber account.
\echo -- Creating a new generic payment method record for the rider
INSERT INTO PaymentMethods (billing_first_name, billing_last_name, billing_zipcode)
VALUES ('Jimmy', 'Fallon', '15289');

\echo
\echo -- Creating an association between the user and that payment method, giving it a nickname.
INSERT INTO UserPaymentMethods (user_id, payment_method_id, payment_method_nickname, date_added)
VALUES ((SELECT MAX(id) FROM Users), (SELECT MAX(id) FROM PaymentMethods), 'Jimmys PayPal', CURRENT_TIMESTAMP );

\echo
\echo -- Detailing the payment method as a PayPal account by creating a record with the users paypal info.
INSERT INTO PayPals (payment_method_id, paypal_email, paypal_password)
VALUES ((SELECT Max(id) FROM PaymentMethods), 'jimmyfallon@gmail.com', 'iloveponies');

\echo
\echo -- Finished simple queries.