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
    log.debug("Sending email message: {}".format(message))

    server = smtplib.SMTP(conf.smtpaddress)

    if conf.smtpssl == "true":
        server.starttls()
    if conf.smtplogin and len(conf.smtplogin) > 0:
        log.debug("Logging in to SMTP account..")
        server.login(conf.smtplogin, conf.smtppassword)

    log.debug("Sending email..")
    server.sendmail(conf.emailsender, recipient, message.encode("UTF8"), ['SMTPUTF8'])
    log.debug("Email sent!")

    server.quit()
    log.debug("Done.")
