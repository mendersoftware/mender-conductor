import configargparse


def get_config():
    p = configargparse.ArgParser()
    p.add('-c', '--conductor', required=False, default="http://mender-conductor:8080", help='conductor base url', env_var='CONDUCTOR')
    p.add('--rpi-version', required=False, help='Raspberry Pi 3 version', env_var='RPI_VERSION')
    p.add('--bbb-version', required=False, help='BeagleBone Black version', env_var='BBB_VERSION')
    p.add('--vexpress-version', required=False, help='vexpress-qemu version', env_var='VEXPRESS_VERSION')
    return p.parse_args()
