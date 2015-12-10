/c j9_uber

--- SIMPLE QUERIES ---

-- 1. As a driver, I want to sign up with my car.
INSERT INTO Drivers
VALUES (16, true, 79.9764, 40.4397);

INSERT INTO CarOwnerships
VALUES ((SELECT LAST(id) FROM Drivers), 3, "14D AA8", 26042, "A1032-1243-5783");


-- 2. As an admin, I want to add a new type of car listing into Uber.
INSERT INTO Cars
VALUES ('Honda', 'Civic', 2014, 'X');


-- *** 3. As a rider, I want to sign up.

INSERT INTO Users
VALUES ('jimmyfallon@gmail.com', 'iloveponies', 'Jimmy', 'Fallon', '6104290811', 'USA');

INSERT INTO Riders
VALUES ((SELECT LAST(id) FROM Riders), 179.9764, 140.4397);


-- *** 4. As a driver, I want to set myself as available to give rides.
UPDATE Drivers
SET is_available = true
WHERE id = "2";


-- *** 5. As an admin, I want to view ride history on a particular day.
SELECT *
FROM Rides
WHERE start_datetime = Date.today();


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
VALUES ((SELECT LAST(id) FROM Users), (SELECT LAST(id) FROM PaymentMethods), 'Jimmys PayPal', Date.today() );

INSERT INTO PayPals
VALUES ((SELECT LAST(id) FROM PaymentMethods), 'jimmyfallon@gmail.com', 'iloveponies');



