import time
from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info.Contracts import tenkswap_contract_address, tenkswap_contract_abi, eth_contract_address, eth_contract_abi, \
    usdt_contract_address, usdt_contract_abi

# 10kSwap合约以及合约使用者
tenkswap_contract = Contract(provider=Accounts.main_account1, address=tenkswap_contract_address,
                             abi=json.loads(tenkswap_contract_abi))
# 代币合约
eth_contract = Contract(provider=Accounts.main_account1, address=eth_contract_address,
                        abi=json.loads(eth_contract_abi))
usdt_contract = Contract(provider=Accounts.main_account1, address=usdt_contract_address,
                         abi=json.loads(usdt_contract_abi))
# 交易的USDT代币数
usdt_amount = int(1 * 10 ** 6)
# 交换路径
path = [Contracts.usdt_contract_address, Contracts.eth_contract_address]


async def tenk_swap():
    # 批准合约使用USDT代币
    usdt_approval = usdt_contract.functions["approve"].prepare(
        Contracts.tenkswap_contract_address,
        usdt_amount,
        max_fee=int(0.0001 * 10 ** 18)
    )
    amounts_out = await tenkswap_contract.functions['getAmountsOut'].call(amountIn=usdt_amount, path=path)
    amount_out = amounts_out.as_dict()['amounts'][1]
    print(amount_out)
    slippage = 0.01
    amount_out_min = int(int(amount_out) * (1 - slippage))
    # 将USDT代币转为ETH代币
    transaction = tenkswap_contract.functions["swapExactTokensForTokens"].prepare(
        amountIn=usdt_amount,
        amountOutMin=amount_out_min,
        path=path,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )

    print('TenkSwap开始进行交换代币:')
    invocation = await Accounts.main_account1.execute([usdt_approval, transaction], max_fee=int(0.0004 * 10 ** 18))
    print('Swap Hash: ' + Web3.to_hex(invocation.transaction_hash))

# asyncio.run(tenk_swap())
