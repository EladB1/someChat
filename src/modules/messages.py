from flask import Blueprint, render_template, escape, request
from flask_socketio import emit
import json

# Import socketio object from ../../main.py
from ..main import socketio

chats = Blueprint('chats', __name__, template_folder='../templates', static_folder='../static')

@chats.route('/')
@chats.route('/home')
def home():
  return render_template('index.html.j2')

# Will eventually move the socketio functions in ../../main.py here
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
  emit('deliver_message', {'data': escape(msg['data'])})

