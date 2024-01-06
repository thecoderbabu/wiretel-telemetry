import smtplib
import local_config as config
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_mail(from_email, to_email, subject, content, filename, file_name):
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, "plain"))

    msg['From'] = "{} <{}>".format("Data Usage", from_email)
    msg['To'] = ','.join(to_email)
    msg['Subject'] = subject
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_name}",
    )
    msg.attach(part)
    s = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(config.HOTMAIL_USERNAME, config.HOTMAIL_PASSWORD)
    s.send_message(msg)
    s.quit()

