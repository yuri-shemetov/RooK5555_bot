import requests
import os
from contextlib import suppress
from subprocess import Popen, PIPE, DEVNULL, CREATE_NEW_PROCESS_GROUP, CREATE_NO_WINDOW
from requests import Session
import platform
from getpass import getpass
from pathlib import Path
from requests.auth import HTTPDigestAuth
from pprint import pprint

# resources
# https://monerodocs.org/interacting/monerod-reference/
# https://www.getmonero.org/resources/developer-guides/wallet-rpc.html
# https://monero-python.readthedocs.io/en/latest/


os.environ['XMR_WALLET'] = 'wallets/stagenet_one/stagenet_one'
os.environ['SIMPLE_PWD'] = 'y4Qm3gPinXtlxqWURi+f8w=='

MAIN_NET_DAEMON = 'http://node.supportxmr.com:18081'  # --untrusted-daemon
STAGENET_DAEMON = 'http://stagenet.xmr-tw.org:38081'  # --untrusted-daemon
XMR_RPC_PORT = os.getenv('XMR_RPC_PORT', '28088')
XMR_RPC_ENDPOINT = f'http://127.0.0.1:{XMR_RPC_PORT}/json_rpc'  # default: http://127.0.0.1:28088/json_rpc
ACCOUNT = 0


# parse .env file
with suppress(FileNotFoundError):
    with open('.env', encoding='utf-8') as dot_env_file:
        for line in iter(lambda: dot_env_file.readline().strip(), ''):
            if not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value


assert 'MONERO' in os.environ


def is_running(look_for, add_exe=True):
    if platform.system() == 'Windows':
        if not look_for.endswith('.exe') and add_exe:
            look_for += '.exe'
        cmd = f'tasklist /NH /FI "IMAGENAME eq {look_for}"'
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=DEVNULL, text=True)
        p.stdout.readline()
        for _ in iter(lambda: p.stdout.readline().strip(), ''): return True
    else:  # Linux
        p = Popen('ps h -C monerod -o comm', stdout=PIPE, stdin=PIPE, stderr=DEVNULL, text=True)
        return p.stdout.readline().strip() != ''
    return False


def is_dev():
    # in reality, return if os.getenv('FLASK_ENV', 'development') == 'development'
    return True


def start_monero_wallet_rpc(monero_rpc=Path(os.environ['MONERO']) / 'monero-wallet-rpc', check_if_running=False):
    """
    Starts monero-wallet-rpc
    ---
    How to create a stagenet wallet:
    Add Monero binaries to %PATH%
    Windows: `cd %HOMEPATH%/Documents/Monero/wallets && mkdir stagenet_one && cd stagenet_one`
    Unix:    `cd ~/Documents/Monero/wallets && mkdir stagenet_one && cd stagenet_one`
    Run: monero-wallet-cli --stagenet --daemon-address=http://stagenet.xmr-tw.org:38081 --untrusted-daemon
    Enter wallet name: stagenet_one
    Enter: "y"

    For only start:
    ---
    monero-wallet-rpc --stagenet --daemon-address=http://stagenet.xmr-tw.org:38081 --wallet-file stagenet_one --password "18051990" --rpc-bind-port 28088
    """
    if check_if_running:
        with suppress(requests.RequestException):
            return requests.post(f'http://127.0.0.1:{XMR_RPC_PORT}/json_rpc',
                                 json={'jsonrpc': '2.0', 'id': '0', 'method': 'get_version'}, timeout=3)
        if is_running(monero_rpc.name):
            return
    rpc_wallet_log = 'other_files/monero-wallet-rpc.log'
    monero_rpc_cmd = [monero_rpc, '--non-interactive', '--log-file', rpc_wallet_log,
                      '--max-log-file-size', '5000000',  # 5MB log size limit
                      '--max-log-files', '1', '--wallet-file', os.environ['XMR_WALLET'], '--log-level', '0',
                      '--rpc-login', 'monero:' + os.environ['SIMPLE_PWD'], '--password']
    if is_dev():
        wallet_pw = getpass('Enter Monero Wallet Password: ')
        monero_rpc_cmd.extend((wallet_pw, '--rpc-bind-port', XMR_RPC_PORT, '--stagenet'))
        monero_rpc_cmd.extend(('--untrusted-daemon', '--daemon-address', STAGENET_DAEMON))
    else:
        monero_rpc_cmd.extend((os.environ['XMR_WALLET_PW'], '--config-file', 'other_files/monero-wallet-rpc.conf'))
    print('INFO: Starting Monero Wallet RPC')
    Popen(monero_rpc_cmd, stdin=DEVNULL, stdout=DEVNULL, shell=True, start_new_session=True,
          creationflags=CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW)


if not is_dev() and not is_running('monerod'):
    # start daemon if not running
    # in reality, use a monerod.conf file and just supply --config-file monerod.conf
    print('starting monerod')
    MONEROD_CMD = [Path(os.environ['MONERO']) / 'monerod', '--non-interactive']
    if 'XMR_DATA_DIR' in os.environ:
        MONEROD_CMD.append('--data-dir')
        MONEROD_CMD.append(os.environ['XMR_DATA_DIR'])
    Popen(MONEROD_CMD, stdin=DEVNULL, stdout=DEVNULL, shell=True)


start_monero_wallet_rpc()


monero_rpc_session = Session()
monero_rpc_session.auth = HTTPDigestAuth('monero', os.environ['SIMPLE_PWD'])


def xmr_rpc_api(method_name, **params):
    rpc_defaults = {'jsonrpc': '2.0', 'id': '0'}
    if '_in' in params:
        params['in'] = params.pop('_in')
    return monero_rpc_session.post(XMR_RPC_ENDPOINT, json={**rpc_defaults, 'method': method_name, 'params': params})

r = xmr_rpc_api('get_transfers', _in=True, account_index=ACCOUNT, subaddr_indices=[0, 1])
print(r.status_code)
print(r.json())

# get_address Example
r = xmr_rpc_api('get_address', account_index=ACCOUNT, address_indexe=[5])
print(r.status_code)
print(r.json())

r = xmr_rpc_api('get_balance', account_index=ACCOUNT)
print(r.status_code)
print(r.json())

# r = xmr_rpc_api('transfer', destinations=[
#         {"amount":100000000000,"address":"7BnERTpvL5MbCLtj5n9No7J5oE5hHiB3tVCK5cjSvCsYWD2WRJLFuWeKTLiXo5QJqt2ZwUaLy2Vh1Ad51K7FNgqcHgjW85o"},
#         {"amount":200000000000,"address":"75sNpRwUtekcJGejMuLSGA71QFuK1qcCVLZnYRTfQLgFU5nJ7xiAHtR5ihioS53KMe8pBhH61moraZHyLoG4G7fMER8xkNv"}
#     ],
#     account_index=0, subaddr_indices=[0], priority=0,  ring_size=7, get_tx_key=True
#     )
# print(r.status_code)
# print(r.json())

# from monero.wallet import Wallet
# from monero.backends.jsonrpc import JSONRPCWallet
# # wallet = JSONRPCWallet(f'http://localhost:{XMR_RPC_PORT}/json_rpc', 'y4Qm3gPinXtlxqWURi+f8w==')

# # Connect to your Monero wallet
# rpc_url = f'http://localhost:{XMR_RPC_PORT}/json_rpc'  # URL of your Monero wallet RPC
# wallet_password = 'y4Qm3gPinXtlxqWURi+f8w=='  # Replace with your wallet passwor

# # Create a JSONRPCWallet instance
# wallet = JSONRPCWallet(rpc_url, wallet_password)
# # wallet = Wallet(JSONRPCWallet(port=XMR_RPC_PORT))
# balance = wallet.balances()
# print(balance)