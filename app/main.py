from flask import Flask
from dotenv import load_dotenv
import os
from os.path import join
import logging
from termcolor import colored

import static


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
app.config['DEBUG'] = (os.getenv('APP_DEBUG') == 'True')

app.add_url_rule('/', view_func=static.index, methods=['GET'])
app.add_url_rule('/favicon.ico', view_func=static.favicon, methods=['GET'])


logfile = join(os.getenv('LOG_PATH'), 'IKEA-Notifier.log')
logging.basicConfig(filename=logfile,
                    format=f'{colored("[%(asctime)s]", "white", )} {colored("%(levelname)s", "yellow")}: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
