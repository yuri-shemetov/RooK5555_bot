import logging
import requests

from decimal import Decimal
from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet

# Connect to your local wallet RPC
wallet = Wallet(JSONRPCWallet(port=18082))  # Default port for wallet RPC


# Example: Send XMR to an address
def send_xmr(to_address, amount):
    try:
        # Create and send transaction
        tx = wallet.transfer(to_address, amount)
        print(f'Transaction sent! Transaction ID: {tx.transaction_id}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Replace with your recipient's address and amount
recipient_address = 'YOUR_RECIPIENT_ADDRESS'
amount_to_send = 0.1  # Amount in XMR

send_xmr(recipient_address, amount_to_send)


def get_balance():
    url = f"https://apilist.tronscan.org/api/account?address={owner_address}&includeToken=true"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()

    if 'error' in data:
        logging.info(f"Error: {data['error']}")
    else:
        usdt_balance = None
        for token in data['trc20token_balances']:
            if token['tokenName'] == 'Tether USD':
                usdt_balance = round(float(token['balance']) * pow(10, -token['tokenDecimal']), 6)
                break

        if usdt_balance is not None:
            return usdt_balance
        return 0
