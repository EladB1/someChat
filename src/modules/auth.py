from flask import Blueprint, render_template, escape
from bcrypt import gensalt, hashpw, checkpw

# Global import of database connector
from ..db_settings import db_connection_pool as conn_pool

auth = Blueprint('auth', __name__, template_folder='../templates', static_folder='../static')

def hash_password(passwd: str) -> bytes:
  salt = gensalt()
  passwd_b = str.encode(passwd) # Need the type to go from string to bytes
  hashed = hashpw(passwd_b, salt)
  return hashed

def compare_pw(username: str, passwd: str) -> bool:
  query = 'SELECT Password FROM Users WHERE Username = %s'
  try:
    passwd_b = str.encode(passwd) # string to bytes
    stored_hash = conn_pool.read_data(query, args=(username))
    stored = str.encode(stored_hash[0]) # string to bytes
    return checkpw(passwd_b, stored)
  except Exception as err:
    print(f'Password extraction Error: {err}')  

@auth.route('/signup')
def signup():
  pass

@auth.route('/login')
def login():
  pass
