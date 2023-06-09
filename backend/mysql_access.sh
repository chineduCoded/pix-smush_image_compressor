#!/bin/bash

# Read MySQL username from a separate file
source credentials.env
export MYSQL_USER

# Set the MySQL password from a separate file
export MYSQL_PWD=$(cat password.txt)

# Connect to the MySQL database and select a specific database
mysql -u "$MYSQL_USER" -h localhost -e "USE pixsmush_dev_db;"
