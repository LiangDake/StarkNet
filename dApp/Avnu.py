from starknet_py.net.models import StarknetChainId
from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info.Contracts import avnu_contract_address, avnu_contract_abi, eth_contract_address, eth_contract_abi, \
    usdt_contract_address, usdt_contract_abi

# AVNU合约以及合约使用者
avnu_contract = Contract(provider=Accounts.main_account1, address=avnu_contract_address,
                         abi=json.loads(avnu_contract_abi))

# 代币合约
usdt_contract = Contract(provider=Accounts.main_account1, address=usdt_contract_address,
                        abi=json.loads(usdt_contract_abi))
# 将要交易的usdt数量
usdt_amount = int(1 * 10 ** 6)
# 路径
route = [{
    "token_from": Contracts.usdt_contract_address,
    "token_to": Contracts.eth_contract_address,
    "exchange_address": Contracts.myswap_contract_address,
    "percent": 100
}]


# 交换代币函数
async def swap():
    # 批准合约使用USDT代币
    usdt_approval = usdt_contract.functions["approve"].prepare(
        Contracts.avnu_contract_address,
        usdt_amount,
        max_fee=int(0.0001 * 10 ** 18)
    )

    # 将USDT代币转为ETH代币
    transaction = avnu_contract.functions["multi_route_swap"].prepare(
        token_from_address=Contracts.usdt_contract_address,  # ETH<->USDT池
        token_from_amount=usdt_amount,
        token_to_address=Contracts.eth_contract_address,
        token_to_amount=613948178133725,
        token_to_min_amount=0,
        beneficiary=Accounts.account1["Address"],
        integrator_fee_amount_bps=0,
        integrator_fee_recipient=0,
        routes=route
    )

    transaction1 = await Accounts.main_account1.sign_invoke_transaction(
        calls=[usdt_approval, transaction],
        max_fee=int(0.0004 * 10 ** 18),
        cairo_version=1
    )
    estimate = await Accounts.main_account1.client.estimate_fee(transaction1)
    print(estimate.overall_fee)
    print('Avnu开始进行交换代币:')
    invocation = await Accounts.main_account1.execute(
        [usdt_approval, transaction],
        max_fee=int(0.0004 * 10 ** 18),
        cairo_version=1
    )
    print('Swap Hash: ' + Web3.to_hex(invocation.transaction_hash))
asyncio.run(swap())
