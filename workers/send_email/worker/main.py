import logging
import traceback

from conductor.ConductorWorker import ConductorWorker

import config
import send_email

conf = config.get_config()

logs_format='[%(asctime)s] [%(levelname)-8s] %(message)s'
if conf.debug:
    logging.basicConfig(format=logs_format, level=logging.DEBUG)
else:
    logging.basicConfig(format=logs_format, level=logging.INFO)
log = logging.getLogger()


def send_email_task(task):
    try:
        log.info("executing task: " + str(task))
        if not send_email.send_email(task['inputData']['email'], task['inputData']['title'], task['inputData']['body']):
            return {'status': 'FAILED', 'output': {}, 'logs': []}

        # always return this well formed response - status, output, logs
        return {'status': 'COMPLETED', 'output': {}, 'logs': []}

    except:
        log.error("failed to run task: " + str(task))
        log.fatal(traceback.format_exc())

        # optionally fill output/logs
        return {'status': 'FAILED', 'output': {}, 'logs': []}


def main():
    log.info('send_email worker connecting to conductor at {}'.format(conf.conductor))
    cc = ConductorWorker(conf.conductor + "/api", 1, 0.1)

    cc.start('send_email', send_email_task, True)

    return 1


if __name__ == '__main__':
    exit(main())
