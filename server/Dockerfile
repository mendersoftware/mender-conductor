FROM mendersoftware/conductor:1.8.1

# tasks
COPY ./tasks /srv/tasks

# workflows
COPY ./workflows /srv/workflows

# events
COPY ./events /srv/events

# entrypoint direcotry with start_conductor.sh and conductor-load scripts
COPY ./entrypoint /srv

ENTRYPOINT ["/srv/start_conductor.sh"]
