import requests

DOLLAR_BTC = "https://blockchain.com/ru/ticker"


def currency_rate():
    response = requests.get(DOLLAR_BTC)
    try:
        response.raise_for_status()
        res = requests.get(DOLLAR_BTC)
        usd = res.json().get("USD").get("last")
    except:
        usd = ""
    return usd