#!/bin/bash

# Define variables
# Set superuser database credentials
SUPER_USER="postgres"
SUPER_PASSWORD="123456"
DB_HOST="localhost"
SQL_SCRIPT="create_db.sql"
# Run the SQL script
PGPASSWORD="$SUPER_PASSWORD" psql -h "$DB_HOST" -U "$SUPER_USER" -f "$SQL_SCRIPT"