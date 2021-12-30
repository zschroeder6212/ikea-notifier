from flask import Response, request, url_for


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
            return 'INVALID_ZIP', 400
        except InvalidCountryCodeException:
            return 'INVALID_COUNTRY', 400
        except EmailNotValidError:
            return 'INVALID_EMAIL', 400


        self.notifier.send_verification_email(id)
        return 'OK', 200

    def remove_notification(self):
        id = request.args.get('id')
        self.notifier.remove_notification(id)
        return ''

    def verify_notification(self):
        id = request.args.get('id')
        self.notifier.verify_notification(id)
        return ''