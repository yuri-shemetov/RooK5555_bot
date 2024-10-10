import requests

# from bitcoinlib.wallets import Wallet
# from bot_app.my_local_settings import passphrase, wallet_name
from bit import PrivateKey as Key
from bot_app.my_local_settings import private_key


# FEES = "https://api.blockchain.info/mempool/fees"
FEES = "https://mempool.space/api/v1/fees/recommended"


def execute_transaction(dest_address, translation):
    source_k = Key(private_key)
    fee = get_fees()
    if fee < 5:
        tx =  source_k.send([(dest_address, translation, "btc")], fee = 5)
    elif fee > 80:
        tx = source_k.send([(dest_address, translation, "btc")], fee = 80)
    else:
        tx = source_k.send([(dest_address, translation, "btc")])
    return tx


def get_balance_bitcoins():
    source_k = Key(private_key)
    return source_k.get_balance("btc")


# def execute_transaction(dest_address, translation):
#     wallet = Wallet(wallet_name)
#     btc = '{} BTC'.format(translation)
#     wallet.scan()
#     satosh = translation * 10_000_000
#     is_free = wallet.select_inputs(satosh) != []
    
#     if is_free:
#         fee = get_fees()
#         if fee < 10:
#             tx = wallet.send_to(dest_address, btc, offline=False, fee=10)
#         elif fee > 300:
#             tx = wallet.send_to(dest_address, btc, offline=False, fee=300)
#         else:
#             tx = wallet.send_to(dest_address, btc, offline=False)
#         return tx
#     return 


# def get_balance_bitcoins():
#     try:
#         wallet = Wallet(wallet_name)
#     except:
#         wallet = Wallet.create(wallet_name, keys=passphrase, network='bitcoin')
#     wallet.scan()
#     balance = wallet.balance() * 0.000_000_01

#     return balance


def get_fees():
    response = requests.get(FEES)
    try:
        response.raise_for_status()
        fee = response.json().get("fastestFee")
    except:
        fee = 4
    return fee
