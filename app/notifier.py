from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError
from flask import url_for
import smtplib
import sqlite3
import logging
import time
import threading
import ikea
import languages
from uuid import uuid4


class InvalidZipCodeException(Exception):
    pass

class InvalidCountryCodeException(Exception):
    pass


class InvalidArticleListException(Exception):
    pass

class Notifier:
    def __init__(self, db, flask_app, email_username, email_password, interval):
        self.db = db
        self.flask_app = flask_app
        self.email_username = email_username
        self.email_password = email_password
        self.interval = interval
        self.init_db()

    def init_db(self):
        """Create required tables"""
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Notifications (
                                email TEXT,
                                country_code TEXT,
                                zip_code TEXT,
                                state_code TEXT,
                                items TEXT,
                                verified TEXT,
                                last_message_time INTEGER,
                                id TEXT
                            )""")
            conn.commit()

    def send_email(self, source, dest, subject, body):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = source
        msg['To'] = dest

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.email_username, self.email_password)
        s.send_message(msg)
        s.quit()
        logging.info(f'Notification sent to {dest}')

    def send_verification_email(self, id):
        with sqlite3.connect(self.db) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('SELECT * FROM Notifications WHERE id = :id', {'id': id})
                email = dict(cur.fetchall()[0])['email']
                url = url_for('verify_notification', id=id, _external=True)
                
                self.send_email(
                    'IKEA Notifier',
                    email,
                    'Verification',
                    f'Click the following link to verify your email!\n{url}'
                )

    def add_notification(self, email, country_code, zip_code, items):
        country_code = country_code.lower()
        state_code = ikea.get_state_code(zip_code, country_code)
        items = ','.join([''.join(filter(str.isdigit, item)) for item in items])
        id = uuid4().hex

        if(state_code == "INVALID_ZIP"):
            raise InvalidZipCodeException('invalid_zip')

        if country_code not in languages.languages:
            raise InvalidCountryCodeException('invalid_country')

        if(len(items) < 1):
            raise InvalidArticleListException('invalid_article')

        
        valid = validate_email(email)
        email = valid.email

        notification = {
            'email': email,
            'country_code': country_code,
            'zip_code': zip_code,
            'state_code': state_code,
            'items': items,
            'verified': 'False',
            'last_message_time': 0,
            'id': id
        }

        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO Notifications VALUES (
                :email,
                :country_code,
                :zip_code,
                :state_code,
                :items,
                :verified,
                :last_message_time,
                :id
            )""", notification)
            conn.commit()

        logging.info(f'Added {id}')
        return id

    def remove_notification(self, id):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Notifications WHERE id = :id", {'id': id})
            conn.commit()
        logging.info(f'Removed {id}')

    def verify_notification(self, id):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()    
            cur.execute('UPDATE Notifications SET verified = "True" WHERE id = :id', {'id': id})
            conn.commit()
        logging.info(f'Verified {id}')

    def reset_time(self, id):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute('UPDATE Notifications SET last_message_time = :time WHERE id = :id', {
                'time': int(time.time()), 
                'id': id
            })
            conn.commit()

    def send_notification(self, email, id):
        self.reset_time(id)

        with self.flask_app.app_context():
            remove_url = url_for('remove_notification', id=id, _external=True)
            print(remove_url)

        self.send_email(
            'IKEA Notifier',
            email,
            'Items Available!',
            f'One or more items you are watching is available for delivery in your zip code!\nTo turn off notifications click here: {remove_url}'
        )

        logging.info(f'Notifying {email}')

    def notify(self):
        while True:
            with sqlite3.connect(self.db) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('SELECT * FROM Notifications')

                for notification in cur:
                    try:
                        if notification['verified'] != 'True':
                            continue
                        # print( int(time.time()) - notification['last_message_time'])
                        if int(time.time()) - notification['last_message_time'] < self.interval:
                            continue

                        state_code = notification['state_code']
                        country_code = notification['country_code']
                        zip_code = notification['zip_code']
                        id = notification['id']
                        email = notification['email']
                        items = notification['items'].split(',')

                        auth = ikea.get_auth(country_code)
                        cart_id = ikea.get_cart_id(items, zip_code, state_code, country_code, auth)
                        order_id = ikea.get_order_id(cart_id, zip_code, state_code, country_code, auth)
                        availability = ikea.get_availability(order_id, cart_id, country_code, auth)

                        if availability != 'NONE':
                            self.send_notification(email, id)
                    except Exception:
                        logging.exception('Error processing notification {notification["id"]}')

    def run(self):
        notification_thread = threading.Thread(target=self.notify)
        notification_thread.start()
