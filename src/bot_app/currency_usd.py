import requests

DOLLAR_BTC = "https://blockchain.com/ru/ticker"

def currency_rate():
    response = requests.get(DOLLAR_BTC)
    if response.status_code == 200:
        try:
            response.raise_for_status()
            res = requests.get(DOLLAR_BTC)
            usd = res.json().get("USD").get("last")
        except:
            usd = ""
    else:
        response = requests.get("https://whattomine.com/asic.json")
        try:
            response.raise_for_status()
            res = requests.get("https://whattomine.com/asic.json")
            usd = res.json()["coins"]["Bitcoin"]["exchange_rate"]
        except:
            usd = ""
    return usd

# DOLLAR_BTC = "https://whattomine.com/asic.json"


# def currency_rate():
#     response = requests.get(DOLLAR_BTC)
#     try:
#         response.raise_for_status()
#         res = requests.get(DOLLAR_BTC)
#         usd = res.json()["coins"]["Bitcoin"]["exchange_rate"]
#     except:
#         usd = ""
#     return usd
