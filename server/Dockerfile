FROM mendersoftware/conductor:2.11.0

RUN apk update && apk add \
    python3 bash curl

# configs
COPY ./config/* /app/config/

# startup scirpt
COPY ./docker/startup.sh /app/

# tasks
COPY ./tasks /srv/tasks

# workflows
COPY ./workflows /srv/workflows

# events
COPY ./events /srv/events

# entrypoint direcotry with start_conductor.sh and conductor-load scripts
COPY ./entrypoint /srv

ENTRYPOINT ["/srv/start_conductor.sh"]
