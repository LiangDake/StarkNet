from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

import time
from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info.SingleAccount import main_client
from Info.Contracts import tenkswap_contract_address, tenkswap_contract_abi, usdt_contract_address, usdt_contract_abi


async def tenk_swap():
    for i in range(1, 3):
        account_member = 'account' + str(i)
        account = getattr(Accounts, account_member, None)
        main_account = Account(
            client=main_client,
            address=account['Address'],
            key_pair=KeyPair.from_private_key(account['PrivateKey']),
            chain=StarknetChainId.MAINNET,
        )
        # 10kSwap合约以及合约使用者
        tenkswap_contract = Contract(provider=main_account, address=tenkswap_contract_address,
                                     abi=json.loads(tenkswap_contract_abi))
        usdt_contract = Contract(provider=main_account, address=usdt_contract_address,
                                 abi=json.loads(usdt_contract_abi))
        # 交易的USDT代币数
        usdt_amount = int(1 * 10 ** 6)
        # 交换路径
        path = [Contracts.usdt_contract_address, Contracts.eth_contract_address]
        # 批准合约使用USDT代币
        usdt_approval = usdt_contract.functions["approve"].prepare(
            Contracts.tenkswap_contract_address,
            usdt_amount,
            max_fee=int(0.0001 * 10 ** 18)
        )
        # 将USDT代币转为ETH代币
        transaction = tenkswap_contract.functions["swapExactTokensForTokens"].prepare(
            amountIn=usdt_amount,
            amountOutMin=0,
            path=path,
            to=account['Address'],
            deadline=int(time.time() + 60 * 60)
        )

        print('TenkSwap开始进行交换代币:')
        invocation = await main_account.execute([usdt_approval, transaction], max_fee=int(0.0004 * 10 ** 18))
        print('Swap Hash: ' + Web3.to_hex(invocation.transaction_hash))


asyncio.run(tenk_swap())
