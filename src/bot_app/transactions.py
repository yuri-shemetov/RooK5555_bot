import requests

# from bit import PrivateKey as Key
from bitcoinlib.wallets import Wallet
from bot_app.my_local_settings import passphrase


# FEES = "https://api.blockchain.info/mempool/fees"
FEES = "https://mempool.space/api/v1/fees/recommended"


def execute_transaction(dest_address, translation):
    wallet = Wallet('Rook5555_wallet')
    btc = '{} BTC'.format(translation)
    # fee = get_fees()
    # if fee < 10:
    #     tx = wallet.send_to(dest_address, btc, offline=False, fee=10)
    # elif fee > 300:
    #     tx = wallet.send_to(dest_address, btc, offline=False, fee=300)
    # else:
    tx = wallet.send_to(dest_address, btc, offline=False)
    return tx


def get_balance_bitcoins():
    try:
        wallet = Wallet('Rook5555_wallet')
    except:
        wallet = Wallet.create("Rook5555_wallet", keys=passphrase, network='bitcoin', scheme='single')
    wallet.scan()
    balance = wallet.balance() * 0.000_000_01

    return balance


def get_fees():
    response = requests.get(FEES)
    try:
        response.raise_for_status()
        fee = response.json().get("fastestFee")
    except:
        fee = 9
    return fee
