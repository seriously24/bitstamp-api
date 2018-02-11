"""
    Based on official doc : https://www.bitstamp.net/api/
    Private API
"""
from .BitstampBaseApi import BitstampBaseApi
import hmac
import hashlib
import time


class BitstampPrivateApi:
    def __init__(self, customer_id, api_key, api_secret):
        """
        Object to handle calls to Bitstamp's API for a specific account
        :param customer_id: Your Bitstamp's customer ID
        :param api_key: API Key of the account
        :param api_secret: API Secret key of the account
        """
        self.api_key = api_key
        self.customer_id = customer_id
        self.bitstamp_base_http_api = BitstampBaseApi()
        self.api_secret = api_secret

    def account_balance(self, currency_pair):
        endpoint = '/balance/{currency_pair}/'.format(currency_pair=currency_pair)
        return self.send_private_request(endpoint)

    def user_transactions(self, currency_pair, offset=0, limit=100, order='desc'):
        endpoint = '/user_transactions/{currency_pair}/'.format(currency_pair=currency_pair)
        additional_data = {'offset': offset, 'limit': limit, 'order': order}
        return self.send_private_request(endpoint, additional_data=additional_data)

    def open_orders(self, currency_pair):
        endpoint = '/open_orders/{currency_pair}'.format(currency_pair=currency_pair)
        return self.send_private_request(endpoint)

    def order_status(self, order_id):
        endpoint = '/order_status/'
        return self.send_private_request(endpoint, additional_data={'id': order_id}, version=1)

    def cancel_order(self, order_id):
        endpoint = '/cancel_order/'
        return self.send_private_request(endpoint, additional_data={'id': order_id})

    def cancel_all_orders(self):
        endpoint = '/cancel_all_orders/'
        return self.send_private_request(endpoint, version=1)

    def buy_limit_order(self, currency_pair, amount, price, limit_price, daily_order=True):
        endpoint = '/buy/{currency_pair}/'.format(currency_pair=currency_pair)
        additional_data = {'amount': amount, 'price': price, 'limit_price': limit_price, 'daily_order': daily_order}
        return self.send_private_request(endpoint, additional_data=additional_data)

    def buy_market_order(self, currency_pair, amount):
        endpoint = '/market/{currency_pair}/'.format(currency_pair=currency_pair)
        return self.send_private_request(endpoint, additional_data={'amount': amount})

    def sell_limit_order(self, currency_pair, amount, price, limit_price, daily_order=True):
        endpoint = '/sell/{currency_pair}/'.format(currency_pair=currency_pair)
        additional_data = {'amount': amount, 'price': price, 'limit_price': limit_price, 'daily_order': daily_order}
        return self.send_private_request(endpoint, additional_data=additional_data)

    def sell_market_order(self, currency_pair, amount):
        endpoint = '/sell/market/{currency_pair}/'.format(currency_pair=currency_pair)
        return self.send_private_request(endpoint, additional_data={'ammount': amount})

    def withdrawal_requests(self, timedelta=50000000):
        endpoint = '/withdrawal-requests/'
        return self.send_private_request(endpoint, additional_data={'timedelta': timedelta})

    def bitcoin_withdrawal(self, amount, address, instant=True):
        endpoint = '/bitcoin_withdrawal/'
        additional_data = {'amount': amount, 'address': address, 'instant': 1 if instant else 0}
        return self.send_private_request(endpoint, additional_data=additional_data, version=1)

    def bitcoin_deposit_address(self):
        endpoint = '/bitcoin_deposit_address/'
        return self.send_private_request(endpoint, version=1)

    def unconfirmed_bitcoin_deposits(self):
        endpoint = '/unconfirmed_btc/'
        return self.send_private_request(endpoint, version=1)

    def litecoin_withdrawal(self, amount, address):
        endpoint = '/ltc_withdrawal/'
        additional_data = {'amount': amount, 'address': address}
        return self.send_private_request(endpoint, additional_data=additional_data, version=1)

    def litecoin_deposit_address(self):
        endpoint = '/ltc_address/'
        return self.send_private_request(endpoint)

    def eth_withdrawal(self, amount, address):
        endpoint = '/eth_withdrawal/'
        additional_data = {'amount': amount, 'address': address}
        return self.send_private_request(endpoint, additional_data=additional_data, version=1)

    def eth_deposit_address(self):
        endpoint = '/eth_address/'
        return self.send_private_request(endpoint)

    def ripple_withdrawal(self, amount, address, currency):
        endpoint = '/ripple_withdrawal/'
        additional_data = {'amount': amount, 'address': address, 'currency': currency}
        return self.send_private_request(endpoint, additional_data=additional_data, version=1)

    def ripple_deposit_address(self):
        endpoint = '/ripple_address/'
        return self.send_private_request(endpoint, version=1)

    def bch_withdrawal(self, amount, address):
        endpoint = '/bch_withdrawal/'
        additional_data = {'amount': amount, 'address': address}
        return self.send_private_request(endpoint, additional_data=additional_data, version=1)

    def bch_deposit_address(self):
        endpoint = '/bch_address/'
        return self.send_private_request(endpoint)

    def transfer_to_main(self, amount, currency, sub_account=''):
        endpoint = '/transfer-to-main/'
        additional_data = {'amount': amount, 'currency': currency}
        if sub_account:
            additional_data['subAccount'] = sub_account
        return self.send_private_request(endpoint, additional_data=additional_data, version=1)

    def xrp_withdrawal(self, amount, address, destination_tag=''):
        endpoint = '/xrp_withdrawal/'
        additional_data = {'amount': amount, 'address': address}
        if destination_tag:
            additional_data['destination_tag'] = destination_tag
        return self.send_private_request(endpoint, additional_data=additional_data)

    def xrp_deposit_address(self):
        endpoint = '/xrp_address/'
        return self.send_private_request(endpoint)

    def open_bank_withdrawal(self, amount, account_currency, name, iban, bic, address, postal_code, city, country, type,
                             bank_name='', bank_address='', bank_postal_code='', bank_city='', bank_country='', currency='',
                             comment=''):
        endpoint = '/withdrawal/open/'
        additional_data = {'amount': amount, 'account_currency': account_currency, 'name': name, 'iban': iban, 'bic': bic,
                           'address': address, 'postal_code': postal_code, 'city': city, 'country': country, 'type': type}

        if bank_name:
            additional_data['bank_name'] = bank_name
        if bank_address:
            additional_data['bank_address'] = bank_address
        if bank_postal_code:
            additional_data['bank_postal_code'] = bank_postal_code
        if bank_city:
            additional_data['bank_city'] = bank_city
        if bank_country:
            additional_data['bank_country'] = bank_country
        if currency:
            additional_data['currency'] = currency
        if comment:
            additional_data['comment'] = comment

        return self.send_private_request(endpoint, additional_data=additional_data)

    def bank_withdrawal_status(self, withdrawal_id):
        endpoint = '/withdrawal/status/'
        return self.send_private_request(endpoint, additional_data={'withdrawal_id': withdrawal_id})

    def cancel_bank_withdrawal(self, withdrawal_id):
        endpoint = '/withdrawal/cancel/'
        return self.send_private_request(endpoint, additional_data={'withdrawal_id': withdrawal_id})

    def new_liquidation_address(self, liquidation_currency):
        endpoint = '/liquidation_address/new/'
        return self.send_private_request(endpoint, additional_data={'liquidation_currency': liquidation_currency})

    def liquidation_address_info(self, address=''):
        endpoint = '/liquidation_address/info/'
        additional_data = {}
        if address:
            additional_data['address'] = address
        return self.send_private_request(endpoint, additional_data=additional_data)

    def send_private_request(self, endpoint, method='POST', version=2, additional_data={}):
        """
        Sends a request to Bitstamp's privare API with the needed base info (key, signature, nonce) built automatically
        :param endpoint: Bitstamp's API endpoint
        :param method: HTTP method to be used, usually POST
        :param version: Version number of the bitstamp API
        :param additional_data: Any other additional data than the usual key, signature and nonce
        """
        nonce = int(time.time() * 10e6)
        sig = self._build_signature(nonce)
        base_data = {'key': self.api_key, 'signature': sig, 'nonce': nonce}

        if additional_data:
            for i, x in additional_data.items():
                base_data[i] = x

        return self.bitstamp_base_http_api.send_request(endpoint, method=method, data=base_data, version=version)

    def _build_signature(self, nonce):
        message = bytes(str(nonce), encoding='utf8') + bytes(self.customer_id, encoding='utf-8') + \
                  bytes(self.api_key, encoding='utf-8')
        signature = hmac.new(bytes(self.api_secret, 'utf-8'), msg=message, digestmod=hashlib.sha256).hexdigest().upper()
        return signature
