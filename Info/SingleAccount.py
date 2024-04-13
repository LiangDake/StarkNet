import time

from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

# 节点API
test_node_url = "https://starknet-testnet.blastapi.io/f281ef1e-7c99-440c-817f-7c113222e847"
main_node_url = "https://starknet-mainnet.blastapi.io/f281ef1e-7c99-440c-817f-7c113222e847"

test_client = FullNodeClient(test_node_url)
main_client = FullNodeClient(main_node_url)

# Braavos钱包账号地址和私钥
address = [
    0x00c42764228369c292aa41dc2d8df2f79074e093e142ee1e3b36022225591b9b,
    0x04129694b4825c92b21e2111e5049a1706634de04a854518fddab97b4efef9fb,
    0x011e174ef92f557e785af6361d3e19bbd6feab0a55bd9c60b89b1b89a35cdc22

]
private_key = [
    0x035b6883d9922d2db24cc6b63e52dd4bdd202aebc1935952ca4fee39fe76c94c,
    0x0745c4c0e04862ed40517ccf8d57c53ba0645734725ac38c6897318bfa67a690,
    0x54d96a06e01583915b8b02c7db8b9323338de4b1cf092fab0822acb8e74ae0
]

# 下面的不需要
account1 = {'Address': 0x00c42764228369c292aa41dc2d8df2f79074e093e142ee1e3b36022225591b9b,
            'PrivateKey': 0x035b6883d9922d2db24cc6b63e52dd4bdd202aebc1935952ca4fee39fe76c94c}
account2 = {'Address': 0x04129694b4825c92b21e2111e5049a1706634de04a854518fddab97b4efef9fb,
            'PrivateKey': 0x0745c4c0e04862ed40517ccf8d57c53ba0645734725ac38c6897318bfa67a690}

#主网账户
main_account1 = Account(
        client=main_client,
        address=account1['Address'],
        key_pair=KeyPair.from_private_key(account1['PrivateKey']),
        chain=StarknetChainId.MAINNET,
    )

main_account2 = Account(
        client=main_client,
        address=account2['Address'],
        key_pair=KeyPair.from_private_key(account2['PrivateKey']),
        chain=StarknetChainId.MAINNET,
    )

# 测试网账户
test_account1 = Account(
        client=test_client,
        address=account1['Address'],
        key_pair=KeyPair.from_private_key(account1['PrivateKey']),
        chain=StarknetChainId.TESTNET,
    )

test_account2 = Account(
        client=test_client,
        address=account2['Address'],
        key_pair=KeyPair.from_private_key(account2['PrivateKey']),
        chain=StarknetChainId.TESTNET,
    )