import configargparse


def get_config():
    p = configargparse.ArgParser()
    p.add('-c', '--conductor', required=True, help='conductor base url', env_var='CONDUCTOR')
    p.add('--smtpaddress', required=True, help='SMTP server address with port', env_var='SMTP_ADDRESS')
    p.add('--smtplogin', required=True, help='SMTP server login', env_var='SMTP_LOGIN')
    p.add('--smtppassword', required=True, help='SMTP server password', env_var='SMTP_PASSWORD')
    p.add('--emailsender', required=True, help='Email FROM field', env_var='EMAIL_SENDER')
    return p.parse_args()
