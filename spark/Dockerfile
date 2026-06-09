FROM bitnami/spark:3.4.1

USER root

# Install python dependencies for Spark Jobs (e.g. psycopg2 for postgres)
RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip install psycopg2-binary redis confluent-kafka

USER 1001
