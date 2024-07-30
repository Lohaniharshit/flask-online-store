#!/bin/bash

# Define variables
DB_USER="postgres"
DB_SCRIPT="create_db_and_tables.sql"

# Run the SQL script
psql -U $DB_USER -f $DB_SCRIPT
