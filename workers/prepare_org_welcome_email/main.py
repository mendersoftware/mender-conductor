import os
import sys
import logging
from string import Template
import traceback
from conductor.ConductorWorker import ConductorWorker
import config


logging.basicConfig()
log = logging.getLogger('conductor-workers.prepare_org_welcome_email')
log.setLevel(logging.INFO)

conf = config.get_config()

template = None


def prepare_org_welcome_email(task):
    log.info('start')
    try:
        org = task['inputData']['organization']
        email = task['inputData']['username']

        body = template.substitute(email=email)
        title = 'Welcome to the Hosted Mender beta program!'

        return {'status': 'COMPLETED',
                'output': {
                    'title': title,
                    'body': body
                    },
                'logs': []}
    except:
        tb = traceback.format_exc()
        log.error('failed: %s', tb)
        return {'status': 'FAILED',
                'output': {},
                'logs': [tb]}


def main():
    global template
    cd = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(cd, 'template')) as tfile:
        template = Template(tfile.read())

    log.info('connecting to conductor at %s', conf.conductor)
    cc = ConductorWorker(conf.conductor + '/api', 1, 0.1)

    cc.start('prepare_org_welcome_email', prepare_org_welcome_email, True)


if __name__ == '__main__':
    main()
