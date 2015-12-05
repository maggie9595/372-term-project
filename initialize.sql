-- CSV Files located in the csv_data folder in the same directory as this script.

-- Import Users
\COPY Users(email, "password", first_name, last_name, phone_number, country) FROM './csv_data/users.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import Riders
\COPY Riders(user_id) FROM './csv_data/riders.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import Driver
\COPY Drivers(user_id, current_latitude, current_longitude, is_available) FROM './csv_data/drivers.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import Administrators
\COPY Administrators(user_id, title) FROM './csv_data/administrators.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import PaymentMethods
\COPY PaymentMethods(billing_first_name, billing_last_name, billing_zipcode) FROM './csv_data/paymentmethods.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import CreditCards
\COPY CreditCards(id, payment_method_id, card_number, expiration_month, expiration_year, cvv_code) FROM './csv_data/creditcards.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import PayPals
\COPY PayPals(payment_method_id, paypal_email, paypal_password) FROM './csv_data/paypals.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import GoogleWallets
\COPY GoogleWallets(payment_method_id, login_email, login_password) FROM './csv_data/googlewallets.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import UserPaymentMethods
\COPY UserPaymentMethods(user_id, payment_method_id, payment_method_nickname, date_added) FROM './csv_data/userpaymentmethods.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import Cars
\COPY Cars(manufacturer, model, "year", ride_type) FROM './csv_data/cars.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import CarOwnwerships
\COPY CarOwnerships(driver_id, car_id, license_plate, car_mileage, drivers_license_num)FROM './csv_data/carownerships.csv' WITH QUOTE '"' DELIMITER ',' CSV;

-- Import Rides
\COPY Rides(rider_id, driver_id, start_latitude, start_longitude, destination, mileage, start_datetime, end_datetime, payment_method_id, price, datetime_paid) FROM './csv_data/rides.csv' WITH QUOTE '"' DELIMITER ',' CSV;
