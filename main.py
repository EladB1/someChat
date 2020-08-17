from flask import Flask, render_template, escape, request
from flask_socketio import SocketIO, emit
import json, secrets

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

socketio = SocketIO(app)

@app.route('/')
@app.route('/home')
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
  emit('deliver_message', {'data': escape(msg['data'])})


if __name__ == '__main__':
  socketio.run(app)
