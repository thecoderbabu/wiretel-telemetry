
import local_config as config
from mailjet_rest import Client


class Mailjet:
    api_key = config.api_key
    api_secret = config.api_secret
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    @classmethod
    def send(cls, my_email, to_emails, subject, content):

        data = {
          'Messages': [
            {
              "From": {
                "Email": my_email,
                "Name": "Data Usage"
              },
              "To": [
                {
                  "Email": to_emails,
                  "Name": "You"
                }
              ],
              "Subject": subject,
              "TextPart": content,
              "HTMLPart": "<h3>Your Wiretel data usage is </h3><br />"
            }
          ]
        }
        result = cls.mailjet.send.create(data=data)
        return result.status_code, result.json()
