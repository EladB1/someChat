#!/bin/bash

### ATTENTION ###
# This file is to
# be run within the
# database container
###           ###

cred=$(cat /run/secrets/APP_DB_PASSWORD)

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_SUPER_USER" <<-EOSQL
  CREATE USER ${APP_DB_USER} WITH CREATEDB;
  ALTER USER ${APP_DB_USER} WITH PASSWORD '${cred}';
  CREATE DATABASE somechat OWNER ${APP_DB_USER};
EOSQL

# psql -U ${APP_DB_USER} somechat -f file.sql
