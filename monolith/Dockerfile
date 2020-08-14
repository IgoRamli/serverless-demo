FROM python:3

ENV GAE_ENV standard

ENV GCP_PROJECT intern-experiment
ENV PUBSUB_TOPIC_NEW_PRODUCT new-product
ENV PUBSUB_TOPIC_PAYMENT_PROCESS payment-process
ENV GCS_BUCKET intern-experiment-storage
ENV FIREBASE_CONFIG firebase_config.json

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE ${PORT}

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app