import asyncio
import web3
from starknet_py.hash.address import compute_address
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair


private_key=0x01ae46aea16c765b7371162688e768a2a9b2fe1fa3dcc8c5fe871939d23324a9
key_pair = KeyPair.from_private_key(private_key)

print("公钥：" + web3.Web3.to_hex(key_pair.public_key))

implementation_class_hash = int('0x5aa23d5bb71ddaa783da7ea79d405315bafa7cf0387a74f4593578c3e9e6570', 16)
proxy_class_hash = int('0x03131fa018d520a037686ce3efddeab8f28895662f019ca3ca18a626650f7d1e', 16)
selector = int('0x2dd76e7ad84dbed81c314ffe5e7a7cacfb8f4836f01af4e913f275f89a3de1a', 16)
calldata = [key_pair.public_key]

address = compute_address(
            class_hash=proxy_class_hash,
            constructor_calldata=[implementation_class_hash, selector, len(calldata), *calldata],
            salt=key_pair.public_key
        )

print("地址：" + web3.Web3.to_hex(address))

main_node_url = "https://starknet-mainnet.infura.io/v3/1b097c1bd1f540248ae7ea41386bced4"
client = FullNodeClient(main_node_url)
chain = StarknetChainId.MAINNET


async def deploy():
    # 获取余额
    account = Account(
        address=address, client=client, key_pair=key_pair, chain=chain
    )
    balance = await account.get_balance()
    print("余额：" + str(balance))

    # 部署地址
    account_deployment_result = await Account.deploy_account(
        address=address,
        class_hash=proxy_class_hash,
        salt=key_pair.public_key,
        key_pair=key_pair,
        client=client,
        chain=chain,
        constructor_calldata=[implementation_class_hash, selector, len(calldata), *calldata],
        max_fee=int(1 * 10 ** 15),
    )

    # Wait for deployment transaction to be accepted
    await account_deployment_result.wait_for_acceptance()
    # From now on, account can be used as usual
    account = account_deployment_result.account

asyncio.run(deploy())