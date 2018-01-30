"""
    Based on official doc : https://www.bitstamp.net/api/
    Public API
"""
import requests
import logging


class BitstampBaseApi:
    def __init__(self):
        self.base_urls = {
            1: 'https://www.bitstamp.net/api',
            2: 'https://www.bitstamp.net/api/v2'
        }
        self.logger = logging.getLogger(__name__)

    def send_request(self, endpoint, method='GET', json_response=True, version=2, **kwargs):
        """
        Sends an HTTP request to Bitstamp and parses the result as a json
        :param endpoint: Bitstamp endpoint to reach
        :param method: HTTP method to use
        :param json_response: True if the expected result should be json
        :param version: Version number of the bitstamp API
        :return: Response from Bitstamp, or None if not a valid response
        :rtype: dict or str
        """
        try:
            base_url = self.base_urls[version]
        except KeyError:
            raise NotImplementedError("send_request() not implemented for Bitstamp API version {}".format(version))

        try:
            r = requests.request(method=method, url=base_url + endpoint, **kwargs)
        except requests.RequestException as e:
            self.logger.error('Error while accessing Bitstamp HTTP API : {}'.format(e))
            return

        if json_response:
            try:
                return r.json()
            except Exception as e:
                self.logger.error('Not a valid json response from Bitstamp : {}'.format(r))
                return
        else:
            return r

    def ticker(self, currency_pair):
        """
        Get the last data for a given currency pair. Last, Bid, Ask, etc.
        :param currency_pair: btcusd, btceur, etc
        :return: Last, Bid, Ask, etc.
        :rtype: dict
        """
        endpoint = '/ticker/{currency_pair}/'.format(currency_pair=currency_pair)
        return self.send_request(endpoint)

    def hourly_ticker(self, currency_pair):
        """
        Get the last data for a given currency pair, from within an hour. Last, Bid, Ask, etc.
        :param currency_pair: btcusd, btceur, etc
        :return: Last, Bid, Ask, etc.
        :rtype: dict
        """
        endpoint = '/ticker_hour/{currency_pair}/'.format(currency_pair=currency_pair)
        return self.send_request(endpoint)

    def order_book(self, currency_pair):
        """
        Get the current order book. Data structure to be confirmed
        :param currency_pair: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc, ethusd, etheur, ethbtc, bchusd, bcheur, bchbtc
        :return: Order book
        :rtype: dict
        """
        endpoint = '/order_book/{currency_pair}/'.format(currency_pair=currency_pair)
        return self.send_request(endpoint)

    def transactions(self, currency_pair, time='hour'):
        """

        :param currency_pair:
        :param time:
        :return:
        """
        endpoint = '/transactions/{currency_pair}?&time={time}'.format(currency_pair=currency_pair, time=time)
        return self.send_request(endpoint)

    def pairs_info(self):
        """
        Get the list of all tradable pairs on Bitstamp platform, and their info
        :return: Name, url_symbol, base_decimals, counter_decimals, minimum_order, trading, description
        :rtype: dict
        """
        endpoint = '/trading-pairs-info/'
        return self.send_request(endpoint)

    def eur_usd(self):
        """
        EUR/USD conversation rate
        :return: Buy and Sell conversion rate
        """
        endpoint = '/eur_usd/'
        return self.send_request(endpoint)
