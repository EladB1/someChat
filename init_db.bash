#!/bin/bash

### ATTENTION ###
# This file is to
# be run within the
# database container
###           ###

if [[ -f /tmp/.db_init.lock ]]; then
  exit 0; # The database was already initialized, exit successfully
fi

su_cred=$(cat /run/secrets/POSTGRES_PASSWORD)
app_cred=$(cat /run/secrets/APP_DB_PASSWORD)

users=$(psql -v ON_ERROR_STOP=1 "postgresql://postgres:${su_cred}@localhost/postgres" <<-EOSQL
  SELECT usename FROM pg_user;
EOSQL
)
echo "$users" | grep ${APP_DB_USER} > /dev/null
return_code=$?
if [[ $return_code -eq 0 ]]; then
  echo 'Database initialized...nothing to left to do.';
  touch /tmp/.db_init.lock
  exit 0; # User exists, exit successfully
fi
# Create the user and database
psql -v ON_ERROR_STOP=1 "postgresql://postgres:${su_cred}@localhost/postgres" <<-EOSQL
  CREATE USER ${APP_DB_USER} WITH CREATEDB;
  ALTER USER ${APP_DB_USER} WITH PASSWORD '${app_cred}';
  CREATE DATABASE somechat OWNER ${APP_DB_USER};
EOSQL

# psql -U ${APP_DB_USER} somechat -f file.sql
