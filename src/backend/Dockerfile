FROM python:3

ENV GAE_ENV standard

COPY . /src/backend

WORKDIR /src/backend

RUN pip install -r requirements.txt

EXPOSE ${PORT}

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app