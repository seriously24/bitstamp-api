import unittest
from BitstampApi.BitstampBaseHttpApi import BitstampBaseHttpApi
# from BitstampApi.BitstampAccountApi import BitstampAccountApi
# TODO : Implements tests for private API too


class TestBitstampBaseHttpApi(unittest.TestCase):
    def setUp(self):
        self.bitstamp_api = BitstampBaseHttpApi()

    def test_ticker(self):
        data = self.bitstamp_api.ticker('btcusd')
        self.assertTrue(isinstance(data, dict))
        needed_keys = ['timestamp', 'open', 'last', 'low', 'high', 'volume', 'ask', 'bid']
        for key in needed_keys:
            self.assertTrue(key in data)

    def test_order_book(self):
        data = self.bitstamp_api.order_book('btcusd')
        self.assertTrue(isinstance(data, dict))
        needed_keys = ['timestamp', 'bids', 'asks']
        for key in needed_keys:
            self.assertTrue(key in data)
        self.assertTrue(data['bids'], list)
        self.assertTrue(data['bids'][0], list)

    def test_transactions(self):
        data = self.bitstamp_api.transactions('btcusd')
        self.assertTrue(data, list)
        self.assertTrue(data[0], dict)

        needed_keys = ['amount', 'type', 'date', 'price', 'tid']
        for key in needed_keys:
            self.assertTrue(key in data[0])

        data_minute = self.bitstamp_api.transactions('btcusd', time='minute')
        self.assertTrue(len(data) >= len(data_minute))
        # data_day = self.bitstamp_api.get_last_transactions('btcusd', time='day')
        # self.assertTrue(len(data) <= len(data_day))

    def test_hourly_ticker(self):
        data = self.bitstamp_api.hourly_ticker('btcusd')
        needed_keys = ['timestamp', 'open', 'last', 'low', 'high', 'volume', 'ask', 'bid']
        for key in needed_keys:
            self.assertTrue(key in data)

    def test_pairs_infos(self):
        data = self.bitstamp_api.pairs_info()
        needed_keys = ['name', 'url_symbol', 'base_decimals', 'counter_decimals', 'minimum_order', 'trading', 'description']
        for pair_info in data:
            for key in needed_keys:
                self.assertTrue(key in pair_info)

    def test_eur_usd(self):
        data = self.bitstamp_api.eur_usd()
        needed_keys = ['buy', 'sell']
        for key in needed_keys:
            self.assertTrue(key in data)


if __name__ == '__main__':
    unittest.main()
