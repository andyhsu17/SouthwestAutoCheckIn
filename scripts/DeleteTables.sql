SET FOREIGN_KEY_CHECKS = 0;

-- Create a prepared statement to drop all tables
SET @drop_statement = NULL;

SELECT GROUP_CONCAT('DROP TABLE IF EXISTS `', table_name, '`') INTO @drop_statement
FROM information_schema.tables

-- Insert database name here
WHERE table_schema = 'reservations';

-- Execute the drop statement
PREPARE stmt FROM @drop_statement;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET FOREIGN_KEY_CHECKS = 1;

-- test_db is the name of the db
-- command to view all tables
-- DROP VIEW IF EXISTS table_name;
SELECT concat('DROP TABLE IF EXISTS `', table_name, '`;') FROM information_schema.tables WHERE table_schema = 'test_db';