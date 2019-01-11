FROM mendersoftware/conductor:2.2.0

RUN apk update && apk add \
    python3 bash curl

# tasks
COPY ./tasks /srv/tasks

# workflows
COPY ./workflows /srv/workflows

# events
COPY ./events /srv/events

# entrypoint direcotry with start_conductor.sh and conductor-load scripts
COPY ./entrypoint /srv

ENTRYPOINT ["/srv/start_conductor.sh"]
