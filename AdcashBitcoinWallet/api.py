from ninja import NinjaAPI
from AdcashBitcoinWallet.models.Transactions import Transactions
from decimal import Decimal
from django.forms.models import model_to_dict
from AdcashBitcoinWallet.utils.wallet_utils import get_wallet_balance, convert_currency, create_transaction, create_unspent_transaction
from django.http import HttpResponse

api = NinjaAPI()


@api.post('/add_transaction')
def add_transaction(request, amount: Decimal):
    """
    Add a transaction of given EUR amount
    """

    # Request validation

    return create_transaction(amount)


@api.post('/get_wallet_balance')
def get_balance(request):
    """
    Get the current wallet balance in BTC and EUR
    """

    balance_btc = get_wallet_balance()

    balance_eur = convert_currency(balance_btc, 'BTC')

    return {
        "balance_btc": balance_btc,
        "balance_eur": balance_eur
    }


@api.post('/add_funds')
def add_funds(request, amount: Decimal):
    """
    Add funds to the wallet
    """

    return create_unspent_transaction(amount)


@api.get('/get_transaction')
def get_transaction(request, transaction_id: str):
    """
    Get a transaction by its id
    """

    transaction = Transactions.objects.get(transaction_id=transaction_id)

    return model_to_dict(transaction)


@api.get('/get_all_transactions')
def get_all_transactions(request):
    """
    Get all transactions
    """

    transactions = Transactions.objects.all()

    return [model_to_dict(transaction) for transaction in transactions]
