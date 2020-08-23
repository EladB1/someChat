import os
from psycopg2 import pool, DatabaseError, sql, Error as pg_error

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

  # execute query and return a cursor object
  def use_cursor(self, query: str, args=None, multi: bool=False):
    try:
      with self.conn_pool.getconn() as conn:
        if conn:
          #print('Connected to database')
          curr = conn.cursor()
          if args != None and not multi:
            curr.execute(query, args)
          elif args != None and multi:
            curr.executemany(query, args)
          # For the next two conditions, make sure the string is safely formatting against SQL Injections
          elif args == None and not multi:
            curr.execute(query) 
          elif args == None and multi:
            curr.executemany(query)
          return curr, conn # leave the calling function responsible for getting the data and closing the cursor
    except (Exception, DatabaseError) as err:
      if conn:
        self.conn_pool.putconn(conn)
      print(f'Database error: {err}');

  def cleanup(self):
    print('Closing database connection pool')
    self.conn_pool.closeall()

  # Get data; multi defines whether it's one or multiple rows, num is for a certain number of rows
  def read_data(self, query, args=None, multi: bool=False, num: int=None):
    try:
      curr, conn = self.use_cursor(query, args)
      if not curr and not conn:
        raise('Failed to get a valid connection and/or cursor')
      if not multi:
        data = curr.fetchone()
      else:
        if num == None:
          data = curr.fetchall()
        else:
          data = curr.fetchmany(num)
      curr.close()
      self.conn_pool.putconn(conn)
      return data
    except (Exception, pg_error) as err:
      print(f'Failed to read data. Error: {err}\nQuery: `{query}`')

  # Insert, Update, and Delete
  def write_one(self, query, args=None):
    try:
      curr, conn = self.use_cursor(query, args)
      if not curr and not conn:
        raise('Failed to get a valid connection and/or cursor')
      conn.commit()
      curr.close()
      self.conn_pool.putconn(conn)
    except (Exception, pg_error) as err:
      print(f'Failed to write to database. Error: {err}\nQuery: `{query}`')

  # Insert, Update, and Delete; take care of multiple rows at once
  def write_many(self, query, args=None):
    try:
      curr, conn = self.use_cursor(query, args, True)
      if not curr and not conn:
        raise('Failed to get a valid connection and/or cursor')
      conn.commit()
      curr.close()
      self.conn_pool.putconn(conn)
    except(Exception, pg_error) as err:
      print(f'Failed to write to multiple rows of database. Error: {err}\nQuery `{query}`')
