from flask import Blueprint, render_template, escape, request
from bcrypt import gensalt, hashpw, checkpw
import re

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

# Backend validation of user submitted data
def new_username_validation(username: str) -> bool:
  pattern = '^([a-zA-Z][\w!\^\$]+)$'
  match = re.match(pattern, username) # will be None if there is no match
  return match != None

def new_password_validtion(passwd: str) -> bool:
  special_chars = '\x3c\x3e~!,%@_`#=;:&\^\$\-\+\.\*\?\\\/\{\}\[\]\(\)\x22\x27'
  pattern = f'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[{special_chars}])[\w{special_chars}]+$'
  match = re.match(pattern, passwd) # will be None if there is no match
  return match != None

# The regex doesn't need to be too accurately filtered
def email_addr_validation(email: str) -> bool:
  pattern = '^\S+@\S+$'
  match = re.match(pattern, email) # will be None if there is no match
  return match != None

# endpoints
@auth.route('/signup', methods=['GET'])
def signup():
  return render_template('signup.html.j2')

@auth.route('/signup', methods=['POST'])
def register_user():
  data = escape(request.form)
  

@auth.route('/login')
def login():
  return render_template('login.html.j2')
