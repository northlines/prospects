# We need to monkey_patch everything
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

from flask import Flask
from flask_cors import CORS

from core.exceptions import AppException
from core.logger import init_request_metrics, get_logger

import views.webhook as webhook

import os
import json
import logging

#Wait for DB to be ready
from lib.db.check import wait_for_db
wait_for_db()

from core.config import Config

#Initialise FLASK app
app = Flask(__name__)

logging.getLogger("prospects.app").setLevel(logging.ERROR)

app.secret_key = Config.SECRET_KEY
app.config['SECRET_KEY'] = Config.SECRET_KEY

@app.errorhandler(AppException)
def handle_app_exception(e):
    if e.status == 500:
        get_logger().critical(
            f"[AppException - {e.code}] {e.message}",
            exc_info=True
        )

    return json.dumps({
        "error": e.code,
        "message": e.message
    }), e.status

@app.errorhandler(Exception)
def handle_global_exception(e):
    get_logger().critical(
        f"[Exception] {str(e)}",
        exc_info=True
    )

    return json.dumps({
        "error": 'UNKNOWN_EXCEPTION',
        "message": 'Administrators have been informed about this issue. Do not hesitate to report at errors@alpy.store'
    }), 500

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAX_CONTENT_LENGTH'] = 30*1024*1024 #Mb = 1024*1024 (Max of 30MByte)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
app.config["PROPAGATE_EXCEPTIONS"] = False

init_request_metrics(app)

webhookview = webhook.webhookView(app)

@app.route("/version")
def version():
    return json.dumps({
        'status': 0,
        'major': 1,
        'minor': 0
    })

if __name__ == "__main__":
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()