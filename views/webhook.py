import sys
import os
import json

sys.path.append('{}/..'.format(os.path.dirname(__file__)))

from flask import request, g, jsonify

from core.logger import get_logger
from core.config import Config
from core.exceptions import AppException
from lib.services.EmailServices import EmailServices
from lib.services.EventServices import EventServices
from lib.services.ProspectServices import ProspectsServices

from lib.objects.Events import Events

class webhookView():
    def __init__(self, app):
        self.application = app
        app.add_url_rule('/brevo/webhook', 'brevo_webhook', self.webhook, methods=['POST'])

    def webhook(self):
        data = request.json

        event = data.get('event')
        message_id = data.get('message-id')

        email = EmailServices.getByBrevoId(message_id)
        event = Events(
            prospect_id = email.prospect_id,
            email_id = email.id,
            event_type = event,
            metadata = data
        )

        if event == 'unsubscribed':
            ProspectsServices.unsubscribe(email.prospect_id, True)

        e = EventServices.register(event)

        print(f'-- Event received : {e}')

        return '', 200