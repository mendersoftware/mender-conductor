import logging
import smtplib

logging.basicConfig()
log = logging.getLogger('conductor-workers.send_email')
log.setLevel(logging.INFO)


def send_email(recipient, title, body, conf):
    if conf.demo == "true":
        log.info(
            "Demo mode on. Intercepted send email request with recipient: {}\nTitle: {}\nBody:\n{}".format(recipient,
                                                                                                           title, body))
        return
    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(conf.emailsender, recipient, title, body)
    server = smtplib.SMTP(conf.smtpaddress)
    server.ehlo()
    if conf.smtpssl == "true":
        server.starttls()
    if conf.smtplogin and len(conf.smtplogin) > 0:
        server.login(conf.smtplogin, conf.smtppassword)
    server.sendmail(conf.emailsender, recipient, message)
    server.quit()
