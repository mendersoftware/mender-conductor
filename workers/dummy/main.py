import logging
import traceback
from conductor.ConductorWorker import ConductorWorker
import config

logging.basicConfig()
log = logging.getLogger('conductor-workers.dummy')
log.setLevel(logging.INFO)

conf = config.get_config()

def dummy(task):
    try:
        log.info('done')

        # always return this well formed response- status, output, logs
        return {'status': 'COMPLETED',
                'output': {},
                'logs': []}
    except Exception as e:
        log.fatal(traceback.format_exc(e))
        # optionally fill output/logs
        return {'status': 'FAILED',
                'output': {},
                'logs': []}


def main():
    log.info('connecting to conductor at {}'.format(conf.conductor))
    cc = ConductorWorker('http://mender-conductor:8080/api', 1, 0.1)

    cc.start('dummy', dummy, True)


if __name__ == '__main__':
    main()
