--- SIMPLE QUERIES ---

-- 1. As a driver, I want to sign up with my car.
-- *** Current location needs to be stored differently?
INSERT INTO Driver
VALUES ('current_location_value', 'is_available_value', 'user_id_value');


-- 2. As an admin, I want to add a new type of car listing into Uber.
INSERT INTO Car
VALUES ('manufacturer_value', 'model_value', 'year_value', 'ride_type_value');


-- 3. As a rider, I want to sign up.
-- *** Need to insert into both User and Rider tables??
INSERT INTO 


-- 4. As a driver, I want to set myself as available to give rides
UPDATE Driver
SET is_available
WHERE id = 'some_driver_id_value';


-- 5. As an admin, I want to view ride history on a particular day


-- 6. As an admin, I want to view the list of all available drivers in the U.S.
-- *** How to denote in the U.S. from current_location
SELECT *
FROM Driver
WHERE (is_available == true) -- AND (current_location ...need to complete here)


-- 7. As a rider, I want to be able to pay with different payment options



