# Gunicorn configuration file
# Based off of this https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

# Socket to bind to
bind = '0.0.0.0:8000'

# Number of clients that can be waiting to be served
backlog = 2048

# Number of processes for handling requests
workers = 1

# Type of worker to use; https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
worker_class = 'eventlet'

# For eventlet/gevent worker classes. Limits max num of clients a process handles
worker_connections = 1000

# Number of seconds before killing a work if it doesn't notify the master process
timeout = 30

# Number of seconds to wait for next request on Keep-Alive HTTP connection
keepalive = 2

# Print out every line of Python executed when running server
spew = False

daemon = False

# Pass environment variables to execution environment
raw_env = []

app_dir = '/opt/flaskapp'

pidfile = f'{app_dir}/.somechat.pid'

user = 'flaskapp'

group = 'flaskapp'

umask = 0

tmp_upload_dir = None

# Change the name of the process
proc_name = None

## Logs

errorlog = f'{app_dir}/logs/error.log'
#errorlog = '-'
loglevel = 'info'
accesslog = f'{app_dir}/logs/access.log'
#accesslog = '-'
#access_log_format = ''


## Server fork

# Called after worker has been forked
def post_fork(server, worker):
  server.log.info(f'Worker spawned with pid: {worker.pid}')

# Called before forking worker subprocess
def pre_fork(server, worker):
  pass

# Called before forking secondary master process
def pre_exec(server):
  server.log.info('Forking master process')

def when_ready(server):
  server.log.info('Gunicorn server is running. Creating workers...')

def worker_int(worker):
  worker.log.info(f'Worker (pid: {worker.pid}) received an interrupt signal')

def worker_abort(worker):
  worker.log.info(f'Worker (pid: {worker.pid}) received an abort signal (SIGABRT)')
