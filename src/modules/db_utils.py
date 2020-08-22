import os
from psycopg2 import pool, DatabaseError, sql

# Database connector code - still need to decide how to integrate this into the app

def get_db_cred(location: str) -> str:
  try:
    with open(location, 'r') as file_:
      data = file_.read().strip() # using .strip() to remove newline char
      if not data:
        raise Exception(f'Error: \'{location}\' is empty or there was a problem retrieving the contents')
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
      self.cleanup()
  # return a cursor object
  def use_cursor(self, query: str, args=None):
    try:
      with self.conn_pool.getconn() as conn:
        if conn:
          print('Connected to database')
          curr = conn.cursor()
          if args != None:
            curr.execute(query, args)
          else:
            curr.execute(query) # make sure the string is safely formatting against SQL Injections
          return curr # leave the calling function responsible for getting the data and closing the cursor
    except (Exception, DatabaseError) as err:
      print(f'Database error: {err}');

  def cleanup(self):
    print('Closing database connection pool')
    self.conn_pool.closeall()

  # Get one piece of data
  def read_one(self, query, args=None):
    curr = self.use_cursor(query, args)
    data = curr.fetchone()
    curr.close()
    return data
'''
# Used the block below for testing how this would work
if __name__ == '__main__':
  dbpool = db_pool(1, 4)
  data = dbpool.read_one()
  print(data)
  dbpool.cleanup()
'''
