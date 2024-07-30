

--  2. Insert data into the item_audit table
-- INSERT INTO item_audit (item_id, rating, sentiment_score, feedback_date) VALUES
-- (1, 'Aloo Paratha', 0.5, '2024-06-21 14:36:00'),
-- (2, 'Burger', 0.7, '2024-06-21 14:36:00'),
-- (3, 'Bhindi', 0.4, '2024-06-21 14:36:00'),
-- (1, 'Aloo Paratha', 0.6, '2024-06-21 14:36:00'),
-- (2, 'Burger', 0.9, '2024-06-21 14:36:00'),
-- (3, 'Bhindi', 0.8, '2024-06-21 14:36:00');
-- insert into voted_item (id, item_id, user_id, date) values  (5, 56, 50, '2024-06-21 14:30:00')

-- insert into feedback (id,item_id, user_id,rating,comment, sentiment_score,date) values (6, 56, 11, 4, "well cooked!", 0.70, '2024-06-21 14:30:00')
--     CREATE TABLE discarded_item_detailed_feedback (
--     item_id INT,
--     user_id,
--     like string,
--     dislike string,
--     home_recipe
-- );

-- DELETE from feedback where item_id = 6


-- -- Create user_profile table
-- CREATE TABLE user_profile ( 
--     id INTEGER PRIMARY KEY ,
--     email TEXT NOT NULL,
--     role_id INTEGER,
--     diet VARCHAR(50),
--     spice_level INTEGER,
--     FOREIGN KEY (role_id) REFERENCES role(id)
-- );

-- -- Create meal_property table
-- CREATE TABLE meal_property (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     item_id INTEGER ,
--     diet VARCHAR(50),
--     spice_level INTEGER,
--     FOREIGN KEY (item_id) REFERENCES item(id)
-- );   

-- Insert dummy data into user_profile table

-- INSERT INTO user_profile (id,email, role_id, diet, spice_level) VALUES
-- ( 1,'rydam@gmail.com', 1, 'vegetarian', 3),
-- ( 2,'hemish@gmail.com', 2, 'eggetarian', 2),
-- ( 3,'nidhi@gmail.com', 3, 'vegetarian', 3),
-- ( 4,'naman@gmail.com', 3, 'non-vegetarian', 3),
-- ( 5,'kashish@gmail.com', 3, 'eggetarian', 3),
-- ( 6,'ahana@gmail.com', 3, 'non-vegetarian', 2),
-- ( 7,'tanish@gmail.com', 3, 'vegetarian', 1);

--  INSERT INTO item (id, name, price, meal_type_id, availability_status) VALUES 
--  (6, 'Egg curry', 140.00, 1, 1), (7, 'Egg sandwhich', 80.00, 1, 1),
--   (8, 'Meat', 170.00, 1, 1), (9, 'Chiken tikka', 190.00, 1, 1);


-- -- Insert dummy data into meal_property table
-- INSERT INTO meal_property (item_id, diet, spice_level) VALUES
-- (1, 'vegetarian', 3),
-- (2, 'vegetarian', 1),
-- (3, 'vegetarian', 3),
-- (4, 'vegetarian', 2),
-- (5, 'vegetarian', 1),
-- (56, 'vegetarian', 2),
-- (6, 'eggetarian', 2),
-- (7, 'eggetarian', 3),
-- (8, 'non-vegetarian', 3),
-- (9, 'non-vegetarian', 1);


-- INSERT INTO rolled_out_item (item_id, item_name, meal_type_id, date) VALUES
-- (56, 'chole', 1, '2024-07-14'),
-- (1, 'Aloo Paratha',  1, '2024-07-14'),
-- (2, 'Burger', 1, '2024-07-14'),
-- -- (9, 'Chiken tikka', 1, '2024-07-14');