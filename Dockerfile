FROM python:3-alpine

# RUN apk --update add python3-dev, postgresql-client, postgresql-dev, build-base
RUN adduser -D django
ENV PATH=$PATH:/home/django/.local/bin
USER django
WORKDIR /usr/src/

COPY requirements.txt ./
RUN pip install -r requirements.txt
ARG IMAGE_VOLUME
VOLUME "$IMAGE_VOLUME" ./images
COPY --chown=django:django . ./

ARG PORT=8000
ARG LOG_LEVEL=info
ENV PORT=$PORT

CMD gunicorn --log-level "${LOG_LEVEL}" --access-logfile - --workers 3 -b "0.0.0.0:$PORT" routsweb.wsgi:application
