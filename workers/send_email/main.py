import logging
import smtplib
import traceback

from conductor.ConductorWorker import ConductorWorker

import config

logging.basicConfig()
log = logging.getLogger('conductor-workers.send_email')
log.setLevel(logging.INFO)

conf = config.get_config()


def send_email(recipient, title, body):
    message = 'From: {}\n Subject: {}\n\n{}'.format(recipient, title, body)
    server = smtplib.SMTP(conf.smtpaddress)
    server.ehlo()
    server.starttls()
    server.login(conf.smtplogin, conf.smtppassword)
    server.sendmail(conf.emailsender, recipient, message)
    server.quit()


def send_email_task(task):
    try:
        send_email(task['inputData']['email'], task['inputData']['topic'], task['inputData']['body'])

        # always return this well formed response- status, output, logs
        return {'status': 'COMPLETED',
                'output': {},
                'logs': []}
    except:
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
