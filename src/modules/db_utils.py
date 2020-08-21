import os
from psycopg2 import pool, DatabaseError, sql

# Database connector code - still need to decide how to integrate this into the app

def get_db_cred(location: str) -> str:
  try:
    with open(location, 'r') as file_:
      data = file_.read().strip() # using .strip() to remove newline char
      if not data:
        raise Exception('Error: \'{location}\' is empty or there was a problem retrieving the contents')
      return data
  except FileNotFoundError:
    print(f'File \'{location}\' could not be found.')
  except IOError as excp:
    print(f'Error reading file \'{location}\': {excp[1]}')

class db_pool:
  def __init__(self, min_conn, max_conn):
    self.min_conn = min_conn
    self.max_conn = max_conn
    try:
      print('Trying to establish database connection pool...')
      self.conn_pool = pool.SimpleConnectionPool(
        self.min_conn,
        self.max_conn,
        host = os.environ['DB_INSTANCE'],
        database = 'somechat',
        user = os.environ['DB_USER'],
        password = get_db_cred(os.environ['DB_PASSWORD_FILE'])
      ) # Start with non-threaded pool version
      if self.conn_pool:
        print(f'Database connection pool established. Min connections: {self.min_conn}, Max connections: {self.max_conn}')
    except (Exception, DatabaseError) as err:
      print(f'Database connection error: {err}')
    finally:
      self.conn_pool.closeall()
      print('Database connection pool closed')
'''
  def use_cursor(self, other_function, *args, **kwargs):
    try:
      with self.conn_pool.getconn() as conn:
        if conn:
          print('Connected to database')
          curr = conn.cursor()
          other_function(self, cursor=curr, *args, **kwargs)

    except (Exception, DatabaseError) as err:
      print(f'Database error: {err}');
'''
