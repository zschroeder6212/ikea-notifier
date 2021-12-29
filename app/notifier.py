from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError
import smtplib
import sqlite3
import logging
import time
import threading
import ikea
import languages
from uuid import uuid4


class Notifier:
    def __init__(self, db, email_username, email_password, interval):
        self.email_username = email_username
        self.email_password = email_password
        self.interval = interval
        self.db = self.init_db()

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

        s = smtplib.SMTP('smtp.gmail.com')
        s.starttls()
        s.login(self.email_username, self.email_password)
        s.send_message(msg)
        s.quit()
        logging.info(f'Notification sent to {dest}')

    def add_notification(self, email, country_code, zip_code, items):
        state_code = ikea.get_state_code(zip_code, country_code)
        items = ','.join(items)
        id = uuid4().hex
        if(state_code == "INVALID_ZIP"):
            return state_code

        if country_code not in languages.languages:
            return "INVALID_COUNTRY"

        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            logging.warning(str(e))
            return "INVALID_EMAIL"

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
        return id

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
                            cur.execute('UPDATE Notifications SET last_message_time = :time WHERE id = :id', {
                                'time': int(time.time()), 
                                'id': id
                            })

                            self.send_email(
                                'IKEA Notifier',
                                email,
                                'Items Available!',
                                'One or more items you are watching are available for delivery in your zip code!'
                            )
                    except Exception as e:
                        logging.warning(f'Error processing notification {notification["id"]}: {str(e)}')

    def run(self):
        notification_thread = threading.Thread(target=self.notify)
        notification_thread.start()
