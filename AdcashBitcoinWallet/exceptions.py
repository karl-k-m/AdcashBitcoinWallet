class CurrencyNotSupported(Exception):
    def __init__(self, currency):
        self.currency = currency
        self.message = f"Currency {currency} is not supported"
