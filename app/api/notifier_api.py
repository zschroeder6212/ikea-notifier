from flask import request
from ikea import InvalidZipCodeException, InvalidCountryCodeException, InvalidArticleListException
from email_validator import EmailNotValidError
import json


class NotifierAPI:
    def __init__(self, notifier):
        self.notifier = notifier

    def add_notification(self):
        try:
            id = self.notifier.add_notification(
                request.json['email'],
                request.json['country_code'],
                request.json['zip_code'],
                request.json['items']
            )
        except InvalidZipCodeException:
            return json.dumps({'code': 'INVALID_ZIP'}), 400
        except InvalidCountryCodeException:
            return json.dumps({'code': 'INVALID_COUNTRY'}), 400
        except EmailNotValidError:
            return json.dumps({'code': 'INVALID_EMAIL'}), 400
        except InvalidArticleListException:
            return json.dumps({'code': 'INVALID_ARTICLES'}), 400
        except Exception:
            return json.dumps({'code': 'UNKNOWN_ERROR'}), 400

        self.notifier.send_verification_email(id)
        return json.dumps({'code': 'OK'}), 200

    def remove_notification(self):
        id = request.args.get('id')
        self.notifier.remove_notification(id)
        return 'REMOVE_OK'

    def verify_notification(self):
        id = request.args.get('id')
        self.notifier.verify_notification(id)
        return 'VERIFY_OK'
