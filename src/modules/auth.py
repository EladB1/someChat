from flask import Blueprint, render_template, escape, request, redirect, flash
from bcrypt import gensalt, hashpw, checkpw
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import re

# Global import of database connector
from ..db_settings import db_connection_pool as conn_pool
from ..main import login_manager
from .user_model import UserModel

auth = Blueprint('auth', __name__, template_folder='../templates', static_folder='../static')


def hash_password(passwd: str) -> bytes:
  salt = gensalt()
  passwd_b = str.encode(passwd) # Need the type to go from string to bytes
  hashed = hashpw(passwd_b, salt)
  return hashed

def compare_pw(userid: int, passwd: str) -> bool:
  query = 'SELECT Password FROM Users WHERE UserID = %s'
  try:
    passwd_b = str.encode(passwd) # string to bytes
    stored_hash = conn_pool.read_data(query, args=[userid])
    stored = str.encode(stored_hash[0]) # string to bytes
    return checkpw(passwd_b, stored)
  except Exception as err:
    print(f'Password extraction Error: {err}')  

def get_userid_by_username(username: str):
  try:
    query = 'SELECT UserID FROM Users WHERE Username = %s'
    userid = conn_pool.read_data(query, args=[username])
    return userid[0]
  except Exception as err:
    print('User ID extraction error: {err}')

def get_userid_by_email(email: str):
  try:
    query = 'SELECT UserID FROM Users WHERE Email = %s'
    userid = conn_pool.read_data(query, args=[email])
    return userid[0]
  except Exception as err:
    print('User ID extraction error: {err}')

# Backend validation of user submitted data
def new_username_validation(username: str) -> bool:
  pattern = '^([a-zA-Z][\w!\^\$]+)$'
  match = re.match(pattern, username) # will be None if there is no match
  return match != None

def new_password_validation(passwd: str) -> bool:
  special_chars = '\x3c\x3e~!,%@_`#=;:&\^\$\-\+\.\*\?\\\/\{\}\[\]\(\)\x22\x27'
  pattern = f'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[{special_chars}])[\w{special_chars}]+$'
  match = re.match(pattern, passwd) # will be None if there is no match
  return match != None

# The regex doesn't need to be too accurately filtered
def email_addr_validation(email: str) -> bool:
  pattern = '^\S+@\S+$'
  match = re.match(pattern, email) # will be None if there is no match
  return match != None

# Sanitize each field of user input (usually forms)
def sanitize_input(user_input):
  for field in user_input:
    field = escape(field)
  return user_input

## TO DO: Handle sending emails

# endpoints
@auth.route('/signup', methods=['GET'])
def signup():
  return render_template('signup.html.j2')

@auth.route('/signup', methods=['POST'])
def register_user():
  data = sanitize_input(request.form)
  valid_username = new_username_validation(data['username'])
  valid_password = new_password_validation(data['password'])
  matching_passwords = data['confirm_password'] == data['password']
  valid_email = email_addr_validation(data['email'])
  if valid_username and valid_email and valid_password and matching_passwords: 
#    return data
    try:
      query = 'INSERT INTO Users(Username, Email, Password) VALUES(%s, %s, %s)'
      insert = conn_pool.write_one(query, [data['username'], data['email'], hash_password(data['password']).decode()])
      flash('Account successfully created')
      return redirect('/login')
    except Exception as err:
      print(f'Authentication error: {err}')
  else:
    flash('Registration error: Please check the information entered')
    return render_template('signup.html.j2')

@auth.route('/login', methods=['GET'])
def login():
  if current_user.is_authenticated:
    flash('You are already logged in.')
    return redirect('/')
  return render_template('login.html.j2')

@auth.route('/login', methods=['POST'])
def authenticate():
  data = sanitize_input(request.form)
  user = UserModel()
  if '@' in data['user']:
    #userid = get_userid_by_email(data['user'])
    user.lookup_by_email(data['user'])
  else:
    #userid = get_userid_by_username(data['user'])
    user.lookup_by_username(data['user'])
  userid = user.userid
  if userid == None:
    flash('Login error: User not found.')
    return render_template('login.html.j2')
  compare = compare_pw(userid, data['password'])
  if compare:
    flash('Login successful')
    login_user(user)
    return redirect('/')
  else:
    flash('Login error: Incorrect password supplied.')
    return render_template('login.html.j2')

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
  if user_id is not None:
    user = UserModel()
    user.lookup_by_userid(user_id)
    return user
  return None

@login_manager.unauthorized_handler
def unauthorized():
  flash('Access denied. Please login')
  return redirect('/login')
