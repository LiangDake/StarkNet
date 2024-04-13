from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info.Contracts import usdt_contract_address, usdt_contract_abi, fibrous_contract_abi, fibrous_contract_address

# Fibrous合约以及合约使用者
fibrous_contract = Contract(provider=Accounts.main_account1, address=fibrous_contract_address,
                            abi=json.loads(fibrous_contract_abi))
# 代币合约
usdt_contract = Contract(provider=Accounts.main_account1, address=usdt_contract_address,
                         abi=json.loads(usdt_contract_abi))
# 将要交易的usdt数量
usdt_amount = int(1 * 10 ** 6)
# 路径
swap = [{
    "token_in": Contracts.usdt_contract_address,
    "token_out": Contracts.eth_contract_address,
    "rate": 1000000,
    "protocol": 2,
    "pool_address": 0x45e7131d776dddc137e30bdd490b431c7144677e97bf9369f629ed8d3fb7dd6  # JediSwap: ETH/USDT Pool

}]

# 字段
params = {
    "token_in": Contracts.usdt_contract_address,
    "token_out": Contracts.eth_contract_address,
    "amount": 1000000,
    "min_received": 0,
    "destination": Accounts.account1["Address"]
}


# 交换代币函数
async def fibrous_swap():
    # 批准合约使用USDT代币
    usdt_approval = usdt_contract.functions["approve"].prepare(
        Contracts.fibrous_contract_address,
        usdt_amount,
        max_fee=int(0.0001 * 10 ** 18)
    )

    # 将USDT代币转为ETH代币
    transaction = fibrous_contract.functions["swap"].prepare(
        swaps=swap,
        params=params
    )

    print('Fibrous开始进行交换代币:')
    invocation = await Accounts.main_account1.execute([usdt_approval, transaction], max_fee=int(0.0005 * 10 ** 18))
    print('Swap Hash: ' + Web3.to_hex(invocation.transaction_hash))


# asyncio.run(fibrous_swap())