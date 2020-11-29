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
  query = 'SELECT UserID, Username FROM Users WHERE UserID != %s'
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
  return render_template('contact.html.j2', userList=users, roomList=rooms)

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

def create_room(name: str, description: str=''):
  write_query = 'INSERT INTO rooms(name, description) VALUES(%s, %s)'
  read_query = 'SELECT roomID WHERE name = %s'
  try:
    insert = conn_pool.write_one(query, [name, description])
    # get the roomID after creating the room
    select = conn_pool.read_data(query, args=[name])
    return select[0]
  except Exception as err:
    print(f'Failed to create room {name} and get its ID. Error: {err}')

# user to user individual chat
@chats.route('/chat/user')
@login_required
def initiate_chat():
  user_info = request.args.to_dict()
  username = user_info['username']
  userid = user_info['userid']
  new_chatroom_name = generate_chat_name()
  description = f'Chat between {current_user.username} and {username}'
  query = 'INSERT INTO room_membership(roomID, UserID) VALUES(%s, %s)'
  try:
    roomID = create_room(name, description)
    add_to_room = conn_pool.write_many(query, [(roomID, current_user.userid), (roomID, userid)])
    return render_template('index.html.j2') # placeholder
  except Exception as err:
    print(f'Could not start chat room: {new_chatroom_name}. Error: {err}')
  
def get_user_room_membership(userid):
  query = 'SELECT room_membership.roomID, name, description FROM room_membership JOIN rooms ON room_membership.roomID = rooms.roomID WHERE userID = %s'
  try:
    rooms = query.read_data(query, args=[userid])
    return rooms
  except Exception as err:
    print(f'Failed to find rooms for UserID: {userid}. Error: {err}')

@chats.route('/chat/<roomid>')
@login_required
def enter_chat(roomid: str):
  return render_template('index.html.j2') # placeholder
