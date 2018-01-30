import unittest
from BitstampApi.BitstampBaseApi import BitstampBaseApi
from BitstampApi.BitstampAccountApi import BitstampAccountApi


class TestBitstampBaseApi(unittest.TestCase):
    def setUp(self):
        self.bitstamp_api = BitstampBaseApi()

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


class TestBitstampPrivateApi(unittest.TestCase):
    """ Only for methods without any impact on the account. i.e no test for sell market order """
    def setUp(self):
        self.bitstamp_private_api = BitstampAccountApi('customer_id', 'api_key', 'api_secret')

    def test_account_balance(self):
        data = self.bitstamp_private_api.account_balance('btcusd')
        self.assertTrue(isinstance(data, dict))
        expected_keys = ['usd_balance','btc_balance','eur_balance','xrp_balance','usd_reserved','btc_reserved','eur_reserved','xrp_reserved','usd_available', 'btc_available','eur_available','xrp_available','btcusd_fee','btceur_fee','eurusd_fee','xrpusd_fee','xrpeur_fee','xrpbtc_fee','fee']
        self._check_keys_in_data(data, expected_keys)

    def test_user_transactions(self):
        data = self.bitstamp_private_api.user_transactions('btcusd')
        self.assertTrue(isinstance(data, list))
        expected_keys = ['datetime','id','type','usd','eur','btc','xrp','btc_usd','fee','order_id']
        self._check_keys_in_data(data, expected_keys)

    def test_open_orders(self):
        data = self.bitstamp_private_api.open_orders('btcusd')
        self.assertTrue(isinstance(data, list))
        expected_keys = ['id','datetime','type','price','amount','currency_pair','Response','status','reason']
        self._check_keys_in_data(data, expected_keys)

    def test_withdrawal_requests(self):
        data = self.bitstamp_private_api.withdrawal_requests()
        self.assertTrue(isinstance(data, list))
        expected_keys = ['id','datetime','type','currency','amount','status']
        self._check_keys_in_data(data, expected_keys)

    def test_litecoin_deposit_address(self):
        data = self.bitstamp_private_api.litecoin_deposit_address()
        self.assertTrue(isinstance(data, str))

    def test_eth_deposit_address(self):
        data = self.bitstamp_private_api.eth_deposit_address()
        self.assertTrue(isinstance(data, str))

    def test_bitcoin_deposit_address(self):
        data = self.bitstamp_private_api.bitcoin_deposit_address()
        self.assertTrue(isinstance(data, str))

    def test_unconfirmed_bitcoin_deposits(self):
        data = self.bitstamp_private_api.unconfirmed_bitcoin_deposits()
        self.assertTrue(isinstance(data, list))

    def test_ripple_deposit_address(self):
        data = self.bitstamp_private_api.ripple_deposit_address()
        self.assertTrue(isinstance(data, str))

    def test_bch_deposit_address(self):
        data = self.bitstamp_private_api.bch_deposit_address()
        self.assertTrue(isinstance(data, str))

    def test_xrp_deposit_address(self):
        data = self.bitstamp_private_api.xrp_deposit_address()
        self.assertTrue(isinstance(data, str))

    def _check_keys_in_data(self, data, expected_keys):
        if isinstance(data, dict):
            for key in expected_keys:
                self.assertTrue(key in data)
        elif isinstance(data, list):
            for item in data:
                for key in expected_keys:
                    self.assertTrue(key in item)
        else:
            raise AssertionError("Data not a dict or list")

if __name__ == '__main__':
    unittest.main()
