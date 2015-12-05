--- SIMPLE QUERIES ---

-- 1. As a driver, I want to sign up with my car.
INSERT INTO Drivers
VALUES (79.9764, 40.4397, true, 2);


-- 2. As an admin, I want to add a new type of car listing into Uber.
INSERT INTO Cars
VALUES ('Honda', 'Civic', 2014, 'X');


-- *** 3. As a rider, I want to sign up.

INSERT INTO Users
VALUES ('jimmy.fallon@gmail.com', 'iloveponies', 'Jimmy', 'Fallon', '6104290811', 'USA');

INSERT INTO Riders
VALUES ('some_user_id_value');


-- *** 4. As a driver, I want to set myself as available to give rides.
UPDATE Drivers
SET is_available
WHERE id = 'some_driver_id_value';


-- *** 5. As an admin, I want to view ride history on a particular day.
SELECT *
FROM Rides
WHERE start_datetime == 'some_datetime_value';


-- 6. As an admin, I want to view the list of all available drivers in the U.S.
SELECT *
FROM Drivers as d
INNER JOIN Users as u
ON d.user_id = u.id
WHERE (d.is_available == true) AND (u.country == 'USA');


-- *** 7. As a rider, I want to link my PayPal account to my Uber account.
INSERT INTO PaymentMethods
VALUES ('Jimmy', 'Fallon', '15289');

INSERT INTO UserPaymentMethods
VALUES (6, 6, 'Jimmys PayPal', 'date_added_value');

INSERT INTO PayPals
VALUES (6, 'jimmy.fallon@gmail.com', 'iloveponies');



