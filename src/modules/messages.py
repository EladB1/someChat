from flask import Blueprint, render_template, escape, request, flash, redirect
from flask_socketio import emit
from flask_login import login_required, current_user
import json

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
  if not current_user.is_authenticated():
    flash('Please login to see contact list.')
    return redirect('/login')
  users = get_user_list(current_user.userid)
  flash(current_user.userid)
  return render_template('contact.html.j2', userList=users)
