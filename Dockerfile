FROM python:3.7-alpine

# Alpine version of adding user
RUN adduser flaskapp -h /opt/flaskapp -D

WORKDIR /opt/flaskapp

RUN chown flaskapp:flaskapp /opt/flaskapp

EXPOSE 8000

RUN python3 -m venv /opt/flaskapp/test-env

COPY requirements.txt /opt/flaskapp

# Alpine dependency installs
RUN apk add gcc musl-dev linux-headers libffi-dev postgresql-dev

# Install other packages
RUN apk add bash pcre pcre-dev

RUN . /opt/flaskapp/test-env/bin/activate && pip install wheel && pip install --upgrade pip

RUN . /opt/flaskapp/test-env/bin/activate && pip install -r requirements.txt

USER flaskapp:flaskapp

# Move over necessary files
COPY src /opt/flaskapp/src

COPY gunicorn.config.py /opt/flaskapp/config.py

# application level logging
RUN mkdir /opt/flaskapp/logs

#CMD . /opt/flaskapp/test-env/bin/activate && python src/main.py

CMD . /opt/flaskapp/test-env/bin/activate && gunicorn --preload --config python:config src.main:app
