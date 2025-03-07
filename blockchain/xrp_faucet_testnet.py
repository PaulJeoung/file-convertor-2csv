import xrpl
from xrpl.wallet import Wallet
from xrpl.constants import CryptoAlgorithm

testnet_url = "https://s.altnet.rippletest.net:51234/"
client = xrpl.clients.JsonRpcClient(testnet_url)
seed = "rsdzt3rarKvMF62mkAa3DwDHaYuQX1mYjk"
accountId = "rQHjWwkpdvy78CxT4mSZNoQNTTFayguawB"

# Example Credentials ----------------------------------------------------------
test_wallet = Wallet.from_seed(seed="sn3nxiW7v8KXzPzAqzyHXbSSKNuN9", algorithm=CryptoAlgorithm.SECP256K1)
print(test_wallet.address) # "rMCcNuTcajgw7YTgBy1sys3b89QqjUrMpH"

def get_account(seed):
    """get_account"""
    client = xrpl.clients.JsonRpcClient(testnet_url)
    print(seed)
    if (seed == ''):
        new_wallet = xrpl.wallet.generate_faucet_wallet(client)
    else:
        new_wallet = xrpl.wallet.Wallet.from_seed(seed)
    return new_wallet

def get_account_info(accountId):
    """get_account_info"""
    acct_info = xrpl.models.requests.account_info.AccountInfo(
    account=accountId,
    ledger_index="validated"
    )
    try:
        response=client.request(acct_info)
    except Exception as e:
        print("오류 발생:", e)
    print(response)
    return response.result['account_data']

# result = get_account_info(seed)
# print(result)