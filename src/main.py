from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
import secrets

# Import code from other modules
#from src.modules.auth import auth

app = Flask(__name__, template_folder='templates', static_folder='static')
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)

#Need to import this below socketio declaration to avoid circular import
from src.modules.messages import chats
# Avoid circular import
from src.modules.auth import auth

# Register blueprints
app.register_blueprint(chats)
app.register_blueprint(auth)

if __name__ == '__main__':
  socketio.run(app)
