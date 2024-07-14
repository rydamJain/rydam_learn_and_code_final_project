

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
    CREATE TABLE discarded_item_detailed_feedback (
    item_id INT,
    user_id,
    like string,
    dislike string,
    home_recipe
);

-- DELETE from rolled_out_item where item_id = 4