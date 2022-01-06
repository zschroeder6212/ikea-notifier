from flask import Flask
from dotenv import load_dotenv
import os
from os.path import join
import logging
from termcolor import colored

import static
from api.countries import get_countries
from notifier import Notifier
from api.notifier_api import NotifierAPI

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
app.config['DEBUG'] = (os.getenv('APP_DEBUG') == 'True')
app.config['SERVER_NAME'] = '192.168.254.229:5000'

notifier = Notifier(os.getenv('DB_FILE'), app, os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'), int(os.getenv('NOTIFICATION_INTERVAL')))
notifier.run()

notifier_api = NotifierAPI(notifier)

app.add_url_rule('/', view_func=static.index, methods=['GET'])
app.add_url_rule('/verification', view_func=static.verification, methods=['GET'])
app.add_url_rule('/favicon.ico', view_func=static.favicon, methods=['GET'])

app.add_url_rule('/api/notifier/add_notification', view_func=notifier_api.add_notification, methods=['POST'])
app.add_url_rule('/api/notifier/verify_notification', view_func=notifier_api.verify_notification, methods=['GET'])
app.add_url_rule('/api/notifier/remove_notification', view_func=notifier_api.remove_notification, methods=['GET'])

app.add_url_rule('/api/get_countries', view_func=get_countries, methods=['GET'])

logfile = join(os.getenv('LOG_PATH'), 'IKEA-Notifier.log')
logging.basicConfig(filename=logfile,
                    format=f'{colored("[%(asctime)s]", "white", )} {colored("%(levelname)s", "yellow")}: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
