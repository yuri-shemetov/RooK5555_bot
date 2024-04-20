# User wallet address
def check_wallet(wallet):
    url_for_view = f"https://www.blockchain.com/ru/btc/address/{wallet}"
    text = url_for_view + "\n"
    return text

# User wallet address for USDT
def check_wallet_usdt(txID):
    url_for_view = f"https://tronscan.org/#/transaction/{txID}"
    text = url_for_view + "\n"
    return text
