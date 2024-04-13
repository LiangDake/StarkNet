from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info.Contracts import (myswap_contract_address, myswap_contract_abi, eth_contract_address, eth_contract_abi,
                            usdt_contract_address, usdt_contract_abi)

# MySwap合约以及合约使用者
myswap_contract = Contract(provider=Accounts.main_account1, address=myswap_contract_address,
                           abi=json.loads(myswap_contract_abi))
# 代币合约
eth_contract = Contract(provider=Accounts.main_account1, address=eth_contract_address,
                        abi=json.loads(eth_contract_abi))
usdt_contract = Contract(provider=Accounts.main_account1, address=usdt_contract_address,
                        abi=json.loads(usdt_contract_abi))
# 将要交易的usdt数量
usdt_amount = int(1 * 10 ** 6)


# 交换代币函数
async def my_swap():
    # 批准合约使用USDT代币
    usdt_contract = Contracts.usdt_contract
    usdt_approval = usdt_contract.functions["approve"].prepare(
        Contracts.myswap_contract_address,
        usdt_amount
    )

    # 将USDT代币转为ETH代币
    transaction = myswap_contract.functions["swap"].prepare(
        pool_id=4,  # ETH<->USDT池
        token_from_addr=Contracts.usdt_contract_address,
        amount_from=usdt_amount,
        amount_to_min=0
    )

    print('MySwap开始进行交换代币:')
    invocation = await Accounts.main_account1.execute([usdt_approval, transaction], max_fee=int(0.0004 * 10 ** 18))
    print('Swap Hash: ' + Web3.to_hex(invocation.transaction_hash))

# asyncio.run(my_swap())