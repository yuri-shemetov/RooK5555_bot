# User wallet address
def check_wallet(tx):
    url_for_view = f"https://mempool.space/ru/tx/{tx}"
    text = url_for_view + "\n"
    return text

# User wallet address for USDT
def check_wallet_usdt(txID):
    url_for_view = f"https://tronscan.org/#/transaction/{txID}"
    text = url_for_view + "\n"
    return text
