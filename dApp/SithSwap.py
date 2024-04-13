import time
from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info.Contracts import eth_contract_address, eth_contract_abi, \
    usdt_contract_address, usdt_contract_abi, sithswap_contract_address, sithswap_contract_abi, myswap_contract_address, \
    myswap_contract_abi

# SithSwap合约以及合约使用者
sithswap_contract = Contract(provider=Accounts.main_account1, address=sithswap_contract_address,
                             abi=json.loads(sithswap_contract_abi))
# MySwap合约以及合约使用者
myswap_contract = Contract(provider=Accounts.main_account1, address=myswap_contract_address,
                           abi=json.loads(myswap_contract_abi))
# 代币合约
eth_contract = Contract(provider=Accounts.main_account1, address=eth_contract_address,
                        abi=json.loads(eth_contract_abi))
usdt_contract = Contract(provider=Accounts.main_account1, address=usdt_contract_address,
                        abi=json.loads(usdt_contract_abi))
# 交易的USDT代币数
usdt_amount = int(1 * 10 ** 6)

# 路径
route = [{
    "from_address": Contracts.usdt_contract_address,
    "to_address": Contracts.eth_contract_address,
    "stable": 1
}]


async def sith_swap():
    # 批准合约使用USDT代币
    usdt_contract = Contracts.usdt_contract
    usdt_approval = usdt_contract.functions["approve"].prepare(
        Contracts.sithswap_contract_address,
        int(2 * 10 ** 6)
    )
    amounts_out = await sithswap_contract.functions['getAmountsOut'].call(amount_in=usdt_amount, routes=route)
    amount_out = amounts_out.as_dict()['amounts'][1]
    print(amount_out)
    slippage = 0.01
    amount_out_min = int(int(amount_out) * (1 - slippage))
    # 将USDT代币转为ETH代币
    sithswap_transaction = sithswap_contract.functions["swapExactTokensForTokensSimple"].prepare(
        amount_in=usdt_amount,
        amount_out_min=amount_out_min,
        token_from=usdt_contract_address,
        token_to=eth_contract_address,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )
    # 将USDT代币转为ETH代币
    myswap_transaction = myswap_contract.functions["swap"].prepare(
        pool_id=4,  # ETH<->USDT池
        token_from_addr=Contracts.usdt_contract_address,
        amount_from=usdt_amount,
        amount_to_min=0
    )
    transaction = await Accounts.main_account1.sign_invoke_transaction(
        calls=[usdt_approval, sithswap_transaction, myswap_transaction],
        max_fee=int(0.0004 * 10 ** 18)
    )
    estimate = await Accounts.main_account1.client.estimate_fee(transaction)
    print(estimate.overall_fee)
    print('SithSwap开始进行交换代币:')
    invocation = await Accounts.main_account1.execute([usdt_approval, sithswap_transaction, myswap_transaction], max_fee=int(0.003 * 10 ** 18))
    print('Swap Hash: ' + Web3.to_hex(invocation.transaction_hash))


asyncio.run(sith_swap())
