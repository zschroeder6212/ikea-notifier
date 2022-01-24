from __future__ import absolute_import
import unittest
import sys
from os import walk
from os.path import join, dirname, abspath, relpath

sys.path.insert(0, abspath(join(dirname(__file__), '../app')))

from main import app
import ikea


class TestCases(unittest.TestCase):
    def test_static_pages(self):
        for root, directories, filenames in walk('app/static'):
            for filename in filenames:
                full_path = join(root, filename)
                relative_path = 'app'
                print(relpath(full_path, relative_path))
                response = app.test_client().get(relpath(full_path, relative_path))
                content = open(full_path, "rb")
                self.assertEqual(content.read(), response.data)
                self.assertEqual(response.status_code, 200)
                content.close()

    def test_index_page(self):
        response = app.test_client().get('/')
        self.assertIn(b"<title>IKEA Notifier</title>", response.data)
        self.assertEqual(response.status_code, 200)

    def test_order(self):
        items = ['50097995']
        country_code = 'us'
        zip_code = '10001'
        state_code = ikea.get_state_code(zip_code, country_code)
        auth = ikea.get_auth(country_code)
        cart_id = ikea.get_cart_id(items, zip_code, state_code, country_code, auth)
        order_id = ikea.get_order_id(cart_id, zip_code, state_code, country_code, auth)
        availability = ikea.get_availability(order_id, cart_id, country_code, auth)

        self.assertEqual(availability, 'FULL')
