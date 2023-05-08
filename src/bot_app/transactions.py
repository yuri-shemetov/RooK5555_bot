import requests

from bit import PrivateKey as Key
from bot_app.my_local_settings import private_key


# FEES = "https://api.blockchain.info/mempool/fees"
FEES = "https://mempool.space/api/v1/fees/recommended"


def execute_transaction(dest_address, translation):
    source_k = Key(private_key)
    fee = get_fees()
    if fee < 25:
        source_k.send([(dest_address, translation, "btc")], fee = 25)
    elif fee > 300:
        source_k.send([(dest_address, translation, "btc")], fee = 300)
    else:
        source_k.send([(dest_address, translation, "btc")])


def get_balance_bitcoins():
    source_k = Key(private_key)
    return source_k.get_balance("btc")


def get_fees():
    response = requests.get(FEES)
    try:
        response.raise_for_status()
        fee = response.json().get("fastestFee")
    except:
        fee = None
    return fee
