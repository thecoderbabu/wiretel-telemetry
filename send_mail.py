import smtplib
import local_config as config
from email.message import EmailMessage


def send_mail(from_email, to_email, subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['From'] = "{} <{}>".format("Data Usage", from_email)
    msg['To'] = ','.join(to_email)
    msg['Subject'] = subject

    s = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(config.HOTMAIL_USERNAME, config.HOTMAIL_PASSWORD)
    s.send_message(msg)
    s.quit()

