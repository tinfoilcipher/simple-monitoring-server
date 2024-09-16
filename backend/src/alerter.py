import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from datetime import datetime
from logger import log_writer

def email_alerter(body, config, logger_config):
    if config["enabled"] is True:
        log_writer(f"Raising Email Alert.", logger_config)
        now = datetime.now()
        alert_time = now.strftime("%d-%m-%Y--%H-%M-%S")
        subject = (f"Monitoring Alert {alert_time}")

        body = '\t\n\n'.join(body) #--Hack alerts on to separate lines
        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = config["sender"]
        message['To'] = config["recipient"]

        # Currently only support local, open SMTP relay without auth. Yuck
        client = smtplib.SMTP(config["server"], config["port"])
        client.send_message(message)
        client.quit()
