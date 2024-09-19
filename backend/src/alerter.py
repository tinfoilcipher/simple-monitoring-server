"""Issues SMTP alerts on detection of an outage."""

import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from logger import log_writer

def email_alerter(body, config, logger_config):
    """Sends body to SMTP client and raises as an email alert
    
    Parameters:
        body (list): SMTP message body as a list of log lines
        config (dict): SMTP client configuration
        logger_config (dict): log_writer configuration
    """
    if config["enabled"] is True:
        try:
            log_writer("Raising Email Alert", logger_config)
            now = datetime.now()
            alert_time = now.strftime("%d-%m-%Y--%H-%M-%S")
            subject = "Monitoring Alert " + alert_time

            body = '\t\n\n'.join(body) #--Hack alerts on to separate lines
            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = config["sender"]
            message['To'] = config["recipient"]

            # Currently only support local, open SMTP relay without auth. Yuck
            client = smtplib.SMTP(config["server"], config["port"])
            client.send_message(message)
            client.quit()
        except Exception as error:
            print(error)
