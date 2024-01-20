#!/bin/bash

source .env
echo "Creating database $DB_NAME"

echo "DROP DATABASE IF EXISTS $DB_NAME; CREATE DATABASE $DB_NAME; ALTER DATABASE $DB_NAME OWNER TO $DB_USER;" | sudo -u postgres psql

python3 -c "from src import init_bd; init_bd()"