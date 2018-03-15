import configargparse


def get_config():
    p = configargparse.ArgParser()
    p.add('-c', '--conductor', required=True, help='conductor base url', env_var='CONDUCTOR')
    p.add('--smtpaddress', required=False, help='SMTP server address with port', env_var='SMTP_ADDRESS')
    p.add('--smtplogin', required=False, help='SMTP server login', env_var='SMTP_LOGIN')
    p.add('--smtppassword', required=False, help='SMTP server password', env_var='SMTP_PASSWORD')
    p.add('--emailsender', required=False, help='Email FROM field', env_var='EMAIL_SENDER')
    p.add('--smtpssl', required=False, help='Should SSL be turned on', env_var='SMTP_SSL')
    p.add('--demo', required=False, help='Demo mode', env_var='DEMO')
    return p.parse_args()
