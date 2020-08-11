FROM python:3.7-alpine

# Alpine version of adding user
RUN adduser flaskapp -h /opt/flaskapp -D

WORKDIR /opt/flaskapp

RUN chown flaskapp:flaskapp /opt/flaskapp

EXPOSE 8000

RUN python3 -m venv /opt/flaskapp/test-env

COPY requirements.txt /opt/flaskapp

# Alpine dependency installs
RUN apk add gcc musl-dev linux-headers libffi-dev postgresql-dev python3-dev

RUN . /opt/flaskapp/test-env/bin/activate && pip install --upgrade pip

RUN . /opt/flaskapp/test-env/bin/activate && pip install -r requirements.txt

COPY main.py /opt/flaskapp
COPY src /opt/flaskapp/src

USER flaskapp:flaskapp

CMD . /opt/flaskapp/test-env/bin/activate && python main.py
