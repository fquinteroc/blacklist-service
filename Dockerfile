FROM python:3.13-slim

WORKDIR /app
RUN mkdir -p /app/src

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Confguración New Relic
RUN pip3 install newrelic
ENV NEW_RELIC_APP_NAME="blacklist-service"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LOG_LEVEL=info
# INGEST_License
ENV NEW_RELIC_LICENSE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

COPY application.py /app/application.py
COPY src /app/src

ARG APP_PORT
ENV PORT=${APP_PORT:-5001}
EXPOSE $PORT

# Para desarrollo
# ENTRYPOINT ["newrelic-admin", "run-program", "python3", "application.py"]

# Para producción
ENTRYPOINT ["newrelic-admin", "run-program", "gunicorn", "--workers=2", "application:app"]
