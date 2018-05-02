import logging
import traceback
import os

from conductor.ConductorWorker import ConductorWorker

import config
import send_email

logging.basicConfig()
log = logging.getLogger('conductor-workers.send_email')

if os.getenv("DEBUG"):
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

conf = config.get_config()


def send_email_task(task):
    try:
        log.debug("running task: " + str(task))
        send_email.send_email(task['inputData']['email'], task['inputData']['title'], task['inputData']['body'], conf)

        # always return this well formed response - status, output, logs
        return {'status': 'COMPLETED',
                'output': {"foo": "bar"},
                'logs': []} 
    except:
        log.debug("failed to run task!")
        log.fatal(traceback.format_exc())

        # optionally fill output/logs
        return {'status': 'FAILED',
                'output': {},
                'logs': []}


def main():
    log.info('send_email worker connecting to conductor at {}'.format(conf.conductor))
    cc = ConductorWorker(conf.conductor + "/api", 1, 0.1)

    cc.start('send_email', send_email_task, True)


if __name__ == '__main__':
    main()
