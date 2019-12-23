FROM mendersoftware/conductor:2.11.0-es6

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

HEALTHCHECK --interval=8s --timeout=15s --start-period=120s --retries=128 CMD curl -f -s -o /dev/null http://127.0.0.1:8080/api/metadata/workflow/decommission_device

ENTRYPOINT ["/srv/start_conductor.sh"]
