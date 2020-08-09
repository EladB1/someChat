FROM python:3.7-stretch

RUN useradd flaskapp -d /opt/flaskapp

WORKDIR /opt/flaskapp

RUN chown flaskapp:flaskapp /opt/flaskapp

RUN pip install --upgrade pip

EXPOSE 8000

RUN python3 -m venv /opt/flaskapp/test-env

COPY requirements.txt /opt/flaskapp

RUN . /opt/flaskapp/test-env/bin/activate && pip install -r requirements.txt

COPY main.py /opt/flaskapp
COPY src /opt/flaskapp/src

USER flaskapp:flaskapp

CMD . /opt/flaskapp/test-env/bin/activate && python main.py
