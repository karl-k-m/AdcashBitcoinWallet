from unittest import TestCase

from AdcashBitcoinWallet.utils.wallet_utils import convert_currency


class Wallet_utils_tests(TestCase):
    def test_create_transaction(self):
        test_json = '{"data":[{"symbol":"BTC/EUR","value":"66936.477715","sources":8,"updated_at":"2024-03-13T19:03:51Z"}'
        test_amount = 100

        btc_amount = convert_currency(test_amount, 'EUR')

