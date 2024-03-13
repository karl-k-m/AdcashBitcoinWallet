from decimal import Decimal

import requests
from django.http import JsonResponse

from AdcashBitcoinWallet.exceptions import CurrencyNotSupported
from AdcashBitcoinWallet.models.Transactions import Transactions


def convert_currency(amount, input_currency):
    """
    Convert between EUR and BTC
    """
    endpoint = 'http://api-cryptopia.adca.sh/v1/prices/ticker'

    try:
        response = requests.get(endpoint)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Failed to fetch the exchange rate"}, status=500)

    data = response.json()

    if input_currency == 'EUR':
        btc_price = next(item for item in data['data'] if item['symbol'] == 'BTC/EUR')['value']
        return Decimal(amount) / Decimal(btc_price)

    if input_currency == 'BTC':
        btc_price = next(item for item in data['data'] if item['symbol'] == 'BTC/EUR')['value']
        return Decimal(amount) * Decimal(btc_price)

    else:
        raise CurrencyNotSupported(input_currency)


def get_wallet_balance():
    """
    Get the current wallet balance in BTC
    """

    transactions = Transactions.objects.all().order_by('-created_at')

    balance = 0

    for transaction in transactions:
        if transaction.spent:
            balance -= transaction.amount
        else:
            balance += transaction.amount
            break

    return balance


def create_transaction(amount):
    """
    Create a transaction
    """

    btc_amount = convert_currency(amount, 'EUR')

    if btc_amount <= 0.00001:
        return JsonResponse({"error": "Amount must be greater than 0.00001"}, status=400)

    wallet_balance = get_wallet_balance()

    if wallet_balance < btc_amount:
        return JsonResponse({"error": "Insufficient funds"}, status=400)

    transaction = Transactions.objects.create(amount=btc_amount)

    Transactions.objects.create(amount=wallet_balance - btc_amount, spent=False)

    return JsonResponse({"transaction_id": transaction.transaction_id}, status=201)


def create_unspent_transaction(amount):
    """
    Create an unspent transaction
    """
    # Request validation

    if amount <= 0:
        return JsonResponse({"error": "Amount must be greater than 0"}, status=400)

    transaction = Transactions.objects.create(amount=amount, spent=False)

    return JsonResponse({"transaction_id": transaction.transaction_id}, status=201)
