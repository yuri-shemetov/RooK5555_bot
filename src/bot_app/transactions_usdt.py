import logging
import requests

import tronpy
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider

from bot_app.my_local_settings import (
    api_key_1, api_key_2, api_key_3,
    contract_address, owner_address, private_key_hex
    )


def create_transaction(dest_address, translation):
    provider = HTTPProvider(api_key=[api_key_1, api_key_2, api_key_3])    
    tron = Tron(provider)
    pk = PrivateKey(bytes.fromhex(private_key_hex))

    abi = [{
        "outputs":[
            {
            "type":"bool"
            }
        ],
        "inputs":[
            {
            "name":"_to",
            "type":"address"
            },
            {
            "name":"_value",
            "type":"uint256"
            }
        ],
        "name":"transfer",
        "stateMutability":"Nonpayable",
        "type":"Function"
    }]
    
    address = pk.public_key.to_base58check_address()
    amount_in_wei = int(translation * 10 ** 6)  # Convert to USDT's decimal precision (6 decimals)
    token_contract = tron.get_contract(contract_address)
    token_contract.abi = abi  
    tx = token_contract.functions.transfer(dest_address, amount_in_wei).with_owner(address).fee_limit(50_000_000).build().sign(pk)
    
    return tx

def execute_transaction(tx):
    tx.broadcast().wait()


def get_balance():
    try:
        url = f"https://apilist.tronscan.org/api/account?address={owner_address}&includeToken=true"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        data = response.json()

        if 'error' in data:
            logging.info(f"Error. Get Balance USDT. {data['error']}")
            provider = HTTPProvider(api_key=[api_key_1, api_key_2, api_key_3]) 
            provider.sess.trust_env = False
            client = Tron(provider)

            contract_usdt = client.get_contract(contract_address)  # usdt
            usdt_balance = round(contract_usdt.functions.balanceOf(owner_address)/ tronpy.TRX, 4)
            return usdt_balance
        else:
            usdt_balance = None
            for token in data['trc20token_balances']:
                if token['tokenName'] == 'Tether USD':
                    usdt_balance = round(float(token['balance']) * pow(10, -token['tokenDecimal']), 6)
                    break

            if usdt_balance:
                return usdt_balance
            return 0
    except Exception as exc:
        logging.warning(f"Error. Get Balance USDT. {exc}")
        provider = HTTPProvider(api_key=[api_key_1, api_key_2, api_key_3]) 
        provider.sess.trust_env = False
        client = Tron(provider)

        contract_usdt = client.get_contract(contract_address)  # usdt
        usdt_balance = round(contract_usdt.functions.balanceOf(owner_address)/ tronpy.TRX, 4)
        return usdt_balance
