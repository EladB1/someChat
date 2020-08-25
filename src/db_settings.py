# Using the file to use database connections across the full app

from src.modules.db_utils import db_pool

min_connections = 1
max_connections = 5
db_connection_pool = db_pool(min_connections, max_connections)
