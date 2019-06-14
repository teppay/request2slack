FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY . /app/

RUN pip install pipenv
RUN pipenv install --system

ENTRYPOINT [ "python", "request2slack.py" ]