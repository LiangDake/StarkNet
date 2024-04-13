import time
from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info.Contracts import (usdt_contract_address, usdt_contract_abi,
                            starkex_contract_address, starkex_contract_abi)

# starkex合约以及合约使用者
starkex_contract = Contract(provider=Accounts.main_account1, address=starkex_contract_address, abi=json.loads(starkex_contract_abi))
# 代币合约
usdt_contract = Contract(provider=Accounts.main_account1, address=usdt_contract_address,
                        abi=json.loads(usdt_contract_abi))
# 交易的USDT代币数
usdt_amount = int(1 * 10 ** 6)
# 交换路径
path = [Contracts.usdt_contract_address, Contracts.eth_contract_address]


async def starkex():
    # 批准合约使用USDT代币
    starkex_usdt_approval = usdt_contract.functions["approve"].prepare(
        spender=Contracts.starkex_contract_address,
        amount=usdt_amount
    )
    # 将USDT代币转为ETH代币
    starkex_transaction = starkex_contract.functions["swapExactTokensForTokens"].prepare(
        amountIn=usdt_amount,
        amountOutMin=0,
        path=path,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )
    print('StarkEx开始进行交换代币:')
    invocation = await Accounts.main_account1.execute([starkex_usdt_approval, starkex_transaction], max_fee=int(0.004 * 10 ** 18))
    print('Swap Hash: ' + Web3.to_hex(invocation.transaction_hash))


asyncio.run(starkex())
