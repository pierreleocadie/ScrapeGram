CREATE TABLE targets_list (
    scrapegram_target_id INT NOT NULL AUTO_INCREMENT,
    instagram_id INT NOT NULL,
    added_on DATETIME NOT NULL,
    PRIMARY KEY (id)
);

-- STORED PROCEDURE
CREATE PROCEDURE add_target(IN instagram_id INT) IS
    BEGIN
        INSERT INTO targets_list (instagram_id, added_on) VALUES (instagram_id, NOW());
    END;

-- CALLING THE STORED PROCEDURE
CALL add_target(123456789);