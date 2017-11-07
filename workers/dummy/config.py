import configargparse

def get_config():
    p = configargparse.ArgParser()
    p.add('-c', '--conductor', required=True, help='conductor base url', env_var='CONDUCTOR')
    return p.parse_args()
