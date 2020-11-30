from flask import Blueprint, render_template, escape, request, flash, redirect
from flask_socketio import emit
from flask_login import login_required, current_user
import json, random, string

# Global import of database connector
from ..db_settings import db_connection_pool as conn_pool

# Import socketio object from ../../main.py
from ..main import socketio, login_manager

chats = Blueprint('chats', __name__, template_folder='../templates', static_folder='../static')


@chats.route('/')
@chats.route('/home')
@login_required
def home():
  return render_template('index.html.j2')

@socketio.on('connect', namespace='/send')
def client_conn_handler():
  print('Connection received')
  emit('connect', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/send')
def client_disconn_handler():
  print('Client disconnected')
  emit('disconnect', {'data': 'Connection to server terminated.'})

@socketio.on('message_event', namespace='/send')
def message_handler(message):
  msg = json.loads(message['payload'])
  emit('deliver_message', {'user': escape(msg['user']), 'data': escape(msg['data']), 'timestamp': escape(msg['timestamp'])}, broadcast=True)

def get_user_list(userid):
  query = 'SELECT UserID, Username FROM Users WHERE UserID != %s ORDER BY Username' # get the sorted version for more efficient searches
  try:
    users = conn_pool.read_data(query, args=[userid], multi=True)
    return users
  except Exception as err:
    print(f'User listing error: {err}')

@chats.route('/contacts')
@login_required
def contact_list():
  users = get_user_list(current_user.userid)
  rooms = get_user_room_membership(current_user.userid)
  if type(rooms) == str:
    flash(rooms)
    rooms = None
  return render_template('contact.html.j2', userList=users, roomList=rooms)

# TODO: Use this endpoint for user search later on
@chats.route('/search/<user_input>')
@login_required
def lookup_user(user_input: str) -> tuple:
  query = 'SELECT UserID, Username FROM Users WHERE UserID != %s AND Username LIKE %s'
  name = f'%{escape(user_input)}%'
  try:
    user = conn_pool.read_data(query, args=[current_user.userid, name])
    if user == None:
      return 'Not found'
    else:
      return json.dumps(user)
  except Exception as err:
    return f'Could not retrieve user. Error: {err}'

#@chats.route('/contacts/<username>')    
#@login_required
# NOTE: Not sure if this is still needed
def user_search(username: str) -> tuple:
  username = escape(username) # not trusting user input
  if username == current_user.username:
    return json.dumps(None)
  query = 'SELECT UserID, Username FROM Users WHERE Username = %s'
  try:
    user = conn_pool.read_data(query, args=[username])
    return json.dumps(user) #render_template('contact.html.j2', userList=[user])
  except Exception as err:
    print(f'User not found: {err}')

def generate_chat_name() -> str:
  length = 12
  name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
  return name

# Since names are auto-generated but descriptions are based on usernames, use those to check for exisiting chats
def individual_chat_exists(description: str, reversed_description: str):
  query = 'SELECT roomID FROM rooms WHERE description = %s'
  try:
    roomID = conn_pool.read_data(query, args=[description])
    if roomID == None:
      roomID = conn_pool.read_data(query, args=[reversed_description])
      if roomID == None:
        return False
    return roomID
  except Exception as err:
    print(f'Failed to get an existing room. Error: {err}')
    return -1

# TODO: Fill this out later
def group_chat_exists():
  pass

def create_room(name: str, description: str=''):
  write_query = 'INSERT INTO rooms(name, description) VALUES(%s, %s)'
  read_query = 'SELECT roomID FROM rooms WHERE name = %s'
  try:
    insert = conn_pool.write_one(write_query, [name, description])
    # get the roomID after creating the room
    select = conn_pool.read_data(read_query, args=[name])
    return select[0]
  except Exception as err:
    print(f'Failed to create room {name} and get its ID. Error: {err}')
    return -1

# user to user individual chat
@chats.route('/chat/user')
@login_required
def initiate_chat():
  user_info = request.args.to_dict()
  username = user_info['username']
  userid = user_info['userid']
  new_chatroom_name = generate_chat_name()
  description = f'Chat between {current_user.username} and {username}'
  alt_description = f'Chat between {username} and {current_user.username}'
  roomID = individual_chat_exists(description, alt_description)
  if roomID:
    if roomID == -1:
      raise Exception('Failed to lookup existing chat')
    else:
      roomID = roomID[0]
    return render_template('index.html.j2') # placeholder
  else:
    query = 'INSERT INTO room_membership(roomID, UserID) VALUES(%s, %s)'
    try:
      roomID = create_room(new_chatroom_name, description)
      if roomID != -1 and roomID != '-1':
        add_to_room = conn_pool.write_many(query, [(roomID, current_user.userid), (roomID, userid)])
        return render_template('index.html.j2') # placeholder
      else:
        raise Exception(f'Failed to get roomID for room {new_chatroom_name}')
    except Exception as err:
      return f'Could not start chat room: {new_chatroom_name}. Error: {err}'
  
def get_user_room_membership(userid):
  query = 'SELECT room_membership.roomID, name, description FROM room_membership JOIN rooms ON room_membership.roomID = rooms.roomID WHERE userID = %s'
  try:
    rooms = conn_pool.read_data(query, args=[userid], multi=True)
    return rooms
  except Exception as err:
    return f'Failed to find rooms for UserID: {userid}. Error: {err}'

@chats.route('/chat/<roomid>')
@login_required
def enter_chat(roomid: str):
  return render_template('index.html.j2') # placeholder
