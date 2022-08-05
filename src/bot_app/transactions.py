import requests

from bit import PrivateKey as Key
from bot_app.my_local_settings import private_key


FEES = "https://api.blockchain.info/mempool/fees"


def execute_transaction(dest_address, translation):
    source_k = Key(private_key)
    t = source_k.send([(dest_address, translation, "btc")])
    print(t)


def get_balance_bitcoins():
    source_k = Key(private_key)
    return source_k.get_balance("btc")


def get_fees():
    response = requests.get(FEES)
    try:
        response.raise_for_status()
        fee = response.json().get("priority")
    except:
        fee = None
    return fee
