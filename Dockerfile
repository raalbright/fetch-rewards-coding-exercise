FROM python:3.8-alpine

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install -d --system

COPY . .

CMD [ "flask", "run", "-h", "0.0.0.0"]