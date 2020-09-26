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

#TODO: Collapse the three lookup functions below into one function

  @classmethod
  def lookup_by_userid(cls, userid):
    user = cls()
    user.userid = userid
    query = 'SELECT Username, Email, status, profile_photo FROM Users WHERE UserID = %s'
    try:
      user_details = conn_pool.read_data(query, args=[userid])
      user.username = user_details[0]
      user.email = user_details[1]
      user.status = user_details[2]
      user.profile_photo = user_details[3]
      return user
    except Exception as err:
      print(f'Error getting user information: {err}')

  @classmethod
  def lookup_by_email(cls, email):
    user = cls()
    user.email = email
    query = 'SELECT UserID, Username, status, profile_photo FROM Users WHERE Email = %s'
    try:
      user_details = conn_pool.read_data(query, args=[email])
      user.userid = user_details[0]
      user.username = user_details[1]
      user.status = user_details[2]
      user.profile_photo = user_details[3]
      return user
    except Exception as err:
      print(f'Error getting user information: {err}')

  @classmethod
  def lookup_by_username(cls, username):
    user = cls()
    user.username = username
    query = 'SELECT UserID, Email, status, profile_photo FROM Users WHERE Username = %s'
    try:
      user_details = conn_pool.read_data(query, args=[username])
      user.userid = user_details[0]
      user.email = user_details[1]
      user.status = user_details[2]
      user.profile_photo = user_details[3]
      return user
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
