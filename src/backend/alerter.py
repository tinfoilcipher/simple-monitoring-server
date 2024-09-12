import smtplib
from email.message import EmailMessage
from datetime import datetime
from logger import log_writer

def email_alerter(body, config):
    if config["enabled"] is True:
        log_writer(f"Raising Email Alert")
        now = datetime.now()
        alert_time = now.strftime("%d-%m-%Y--%H-%M-%S")
        subject = (f"Monitoring Alert {alert_time}")

        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = config["sender"]
        message['To'] = config["recipient"]

        # Currently only support local, open SMTP relay without auth. Yuck
        client = smtplib.SMTP(config["server"], config["port"])
        client.send_message(message)
        client.quit()
