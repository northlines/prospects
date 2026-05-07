# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
import os

sys.path.append('{}/..'.format(os.path.dirname(__file__)))

from core.config import Config

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

class email:
    def __init__(self, mail_address, name):
        self.addr = mail_address
        self.name = name
        
    def send(self, to, subject, htmlMessage):
        # Configure API key authorization
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = Config.BREVO_KEY

        print(Config.BREVO_KEY)

        # Create an instance of the API class
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Email details
        email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to['email'], "name": '{} {}'.format(to['firstname'], to['lastname'])}],  # Recipient details
            sender={"email": self.addr, "name": self.name},  # Sender details
            subject= subject,  # Email subject
            html_content= htmlMessage  # Email content in HTML
        )

        try:
            # Send the email
            response = api_instance.send_transac_email(email)
            print(f"Email sent successfully! Response: {response}")

        except ApiException as e:
            print(f"An error occurred: {e}")
            return -1
        
        return response.message_id
