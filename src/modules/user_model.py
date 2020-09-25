from ..db_settings import db_connection_pool as conn_pool

# class for flask-login login manager to use

class UserModel:
  def __init__(self):
    '''self.is_authenticated = False
    self.is_active = False
    self.is_anonymous = True'''
    self.userid = 0
    self.username = None
    self.email = None
    self.status = None
    self.profile_photo = None

# TODO: replace lookup functions below with constructor(s) that can fetch the user by email, username, or userid

  def lookup_by_userid(self, userid):
    self.userid = userid
    query = 'SELECT Username, Email, status, profile_photo FROM Users WHERE UserID = %s'
    try:
      user_details = conn_pool.read_data(query, args=[email])
      self.username = user_details[0]
      self.email = user_details[1]
      self.status = user_details[2]
      self.profile_photo = user_details[3]
    except Exception as err:
      print(f'Error getting user information: {err}')

  def lookup_by_email(self, email):
    self.email = email
    query = 'SELECT UserID, Username, status, profile_photo FROM Users WHERE Email = %s'
    try:
      user_details = conn_pool.read_data(query, args=[email])
      self.userid = user_details[0]
      self.username = user_details[1]
      self.status = user_details[2]
      self.profile_photo = user_details[3]
    except Exception as err:
      print(f'Error getting user information: {err}')

  def lookup_by_username(self, username):
    self.username = username
    query = 'SELECT UserID, Email, status, profile_photo FROM Users WHERE Username = %s'
    try:
      user_details = conn_pool.read_data(query, args=[username])
      self.userid = user_details[0]
      self.email = user_details[1]
      self.status = user_details[2]
      self.profile_photo = user_details[3]
    except Exception as err:
      print(f'Error getting user information: {err}')
  
  def get_id(self):
    return str(self.userid) # need to convert it to unicode for flask_login function
  def is_authenticated(self):
    return True
  def is_active(self):
    return True
  def is_anonymous(self):
    return False

'''
  def auth_user(self):
    self.is_authenticated = True
    self.is_active = True
    self.is_anonymous = True
'''
