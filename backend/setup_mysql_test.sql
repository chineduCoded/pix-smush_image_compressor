-- Prepares a MySQL server for the project
CREATE DATABASE IF NOT EXISTS pixsmush_test_db;
CREATE USER IF NOT EXISTS 'pixsmush_test'@'localhost' IDENTIFIED BY 'pixsmush_test_pwd';
GRANT ALL PRIVILEGES ON pixsmush_test_db.* TO 'pixsmush_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'pixsmush_test'@'localhost';
FLUSH PRIVILEGES;
