import requests
import local_config as config


class Mailgun:
    MAILGUN_DOMAIN = config.MAILGUN_DOMAIN
    MAILGUN_API_KEY = config.MAILGUN_API_KEY
    FROM_NAME = config.FROM_NAME
    FROM_EMAIL = config.FROM_EMAIL

    @classmethod
    def send(cls, to_emails, subject, content):
        requests.post("https://api.mailgun.net/v3/{}/messages".format(cls.MAILGUN_DOMAIN),
                      auth=("api", cls.MAILGUN_API_KEY),
                      data={"from": "{} <{}>".format(cls.FROM_NAME, cls.FROM_EMAIL),
                            "to": to_emails,
                            "subject": subject,
                            "text": content})
