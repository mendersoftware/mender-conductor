import logging
import smtplib
import traceback
import config


conf = config.get_config()

logs_format='[%(asctime)s] [%(levelname)-8s] %(message)s'
if conf.debug:
    logging.basicConfig(format=logs_format, level=logging.DEBUG)
else:
    logging.basicConfig(format=logs_format, level=logging.INFO)
log = logging.getLogger()


def send_email(recipient, title, body):
    if conf.demo == "true":
        log.info(
            "Demo mode on. Intercepted send email request with recipient: {}\nTitle: {}\nBody:\n{}".format(recipient,
                                                                                                           title, body))
        return

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(conf.emailsender, recipient, title, body)
    log.debug("Sending email message: {}".format(message))

    try:
        server = smtplib.SMTP(conf.smtpaddress)

        if conf.smtpssl == "true":
            server.starttls()
        if conf.smtplogin and len(conf.smtplogin) > 0:
            log.debug("Logging in to SMTP account..")
            server.login(conf.smtplogin, conf.smtppassword)

        log.debug("Sending email..")
        server.sendmail(conf.emailsender, recipient, message.encode("UTF8"), ['SMTPUTF8'])
        log.info("Email successfully sent to '%s'" % recipient)

        return True

    except:
        log.error("Failed to send message to '%s'" % recipient)
        log.fatal(traceback.format_exc())
        return False

    finally:
        server.quit()
