FROM python:3.7-stretch

WORKDIR /opt/flaskapp

EXPOSE 8000

RUN python3 -m venv /opt/flaskapp/test-env

COPY requirements.txt /opt/flaskapp

RUN . /opt/flaskapp/test-env/bin/activate && pip install -r requirements.txt

COPY main.py /opt/flaskapp
COPY src /opt/flaskapp/src

CMD . /opt/flaskapp/test-env/bin/activate && python main.py
