import requests
import json
import languages


def get_state_code(zip_code, country_code):
    r = requests.get(f'https://locations.poc.oc.ingka.com/locationservice/{country_code}/{zip_code}')

    print(r.json())
    if('errorCode' in r.json() and r.json()['errorCode'] == 200001):
        return ''

    if('validZipCode' in r.json() and r.json()['validZipCode'] is False):
        return 'INVALID_ZIP'

    return r.json()['additionalAttributes']['stateInfo'][0]['stateCode']


def get_auth(country_code):
    headers = {
        'X-Client-Secret': 'cP0vA4hJ4gD8kO3vX3fP2nE6xT7pT3oH0gC5gX6yB4cY7oR5mB',
        'Content-Type': 'application/json',
        'X-Client-Id': 'e026b58d-dd69-425f-a67f-1e9a5087b87b'
    }

    data = {
        'retailUnit': country_code
    }

    r = requests.post('https://api.ingka.ikea.com/guest/token', headers=headers, data=json.dumps(data))
    return f"{r.json()['token_type']} {r.json()['access_token']}"


def get_cart_id(items, zip_code, state_code, country_code, auth):
    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
        'X-Client-Id': 'af2525c3-1779-49be-8d7d-adf32cac1934'
    }

    language_code = languages.languages[country_code]

    data = {
        'shoppingType': 'ONLINE',
        'channel': 'WEBAPP',
        'checkoutType': 'STANDARD',
        'languageCode': language_code,
        'items': [],
        'serviceArea': {
            'zipCode': zip_code,
            'stateCode': state_code
        },
        'preliminaryAddressInfo': None
    }

    for item in items:
        data['items'].append({
            'quantity': 1,
            'itemNo': item,
            'uom': 'PIECE'
        })

    r = requests.post(f'https://ordercapture.ingka.com/ordercaptureapi/{country_code}/checkouts', headers=headers, data=json.dumps(data))
    return r.json()['resourceId']


def get_order_id(cart_id, zip_code, state_code, country_code, auth):
    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
        'X-Client-Id': 'af2525c3-1779-49be-8d7d-adf32cac1934'
    }

    data = {
        'zipCode': zip_code,
        'stateCode': state_code
    }

    r = requests.post(f'https://ordercapture.ingka.com/ordercaptureapi/{country_code}/checkouts/{cart_id}/service-area', headers=headers, data=json.dumps(data))
    print(r.json())
    return r.json()['id']


def get_availability(order_id, cart_id, country_code, auth):
    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
        'X-Client-Id': 'af2525c3-1779-49be-8d7d-adf32cac1934'
    }

    r = requests.get(f'https://ordercapture.ingka.com/ordercaptureapi/{country_code}/checkouts/{cart_id}/service-area/{order_id}/home-delivery-services', headers=headers)

    for deliveryServices in r.json()['possibleDeliveryServices']['deliveryServices']:
        if('fulfillmentPossibility' in deliveryServices):
            return deliveryServices['fulfillmentPossibility']

    return "NONE"
