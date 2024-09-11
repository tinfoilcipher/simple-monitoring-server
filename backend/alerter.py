import smtplib
from email.message import EmailMessage
from datetime import datetime

def email_alerter(body, config):
    now = datetime.now()
    alert_time = now.strftime("%d-%m-%Y--%H-%M-%S")
    subject = (f"Monitoring Alert {alert_time}")

    message = EmailMessage()
    message.set_content("THIS IS THE BODY OF MY EMAIL")
    message['Subject'] = subject
    message['From'] = config["sender"]
    message['To'] = config["recipient"]

    # Currently only support local, open SMTP relay without auth. Yuck
    client = smtplib.SMTP(config["server"], config["port"])
    client.send_message(message)
    client.quit()
