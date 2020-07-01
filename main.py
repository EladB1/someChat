from flask import Flask, escape, render_template, request;
import json;
app = Flask(__name__, static_folder='src/static', template_folder='src/templates');

@app.route('/')
@app.route('/home')
def homepage():
  return render_template('index.html.j2');

@app.route('/send', methods=['POST'])
def handleMessage():
  msg = request.json['message'];
  return json.dumps(escape(msg));

if __name__ == '__main__':
  app.run('0.0.0.0', 8000, debug=True);
