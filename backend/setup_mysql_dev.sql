-- Prepares a MySQL server for the project
CREATE DATABASE IF NOT EXISTS pixsmush_dev_db;
CREATE USER IF NOT EXISTS 'pixsmush_dev'@'localhost' IDENTIFIED BY 'pixsmush_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'pixsmush_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'pixsmush_dev'@'localhost';
FLUSH PRIVILEGES;