import time
from web3 import Web3
import asyncio
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info import Contracts
from Info.Contracts import (eth_contract_address, usdt_contract_address, usdt_contract_abi,
                            sithswap_contract_address, sithswap_contract_abi,
                            myswap_contract_address, myswap_contract_abi,
                            jediswap_contract_address, jediswap_contract_abi,
                            fibrous_contract_address, fibrous_contract_abi,
                            tenkswap_contract_address, tenkswap_contract_abi,
                            protoss_contract_address, protoss_contract_abi,
                            starkex_contract_address, starkex_contract_abi)
b
# SithSwap合约以及合约使用者
sithswap_contract = Contract(provider=Accounts.main_account1, address=sithswap_contract_address,
                             abi=json.loads(sithswap_contract_abi))
# MySwap合约以及合约使用者
myswap_contract = Contract(provider=Accounts.main_account1, address=myswap_contract_address,
                           abi=json.loads(myswap_contract_abi))
# JediSwap合约以及合约使用者
jediswap_contract = Contract(provider=Accounts.main_account1, address=jediswap_contract_address,
                             abi=json.loads(jediswap_contract_abi))
# 10kSwap合约以及合约使用者
tenkswap_contract = Contract(provider=Accounts.main_account1, address=tenkswap_contract_address,
                             abi=json.loads(tenkswap_contract_abi))
# Fibrous合约以及合约使用者
fibrous_contract = Contract(provider=Accounts.main_account1, address=fibrous_contract_address,
                            abi=json.loads(fibrous_contract_abi))
# starkex合约以及合约使用者
starkex_contract = Contract(provider=Accounts.main_account1, address=starkex_contract_address,
                            abi=json.loads(starkex_contract_abi))
# protoss合约以及合约使用者
protoss_contract = Contract(provider=Accounts.main_account1, address=protoss_contract_address,
                            abi=json.loads(protoss_contract_abi))

# USDT合约以及每一笔交易的USDT代币数
usdt_contract = Contract(provider=Accounts.main_account1, address=usdt_contract_address,
                        abi=json.loads(usdt_contract_abi))
usdt_amount = int(1 * 10 ** 6)

# JediSwap交换路径
path = [Contracts.usdt_contract_address, Contracts.eth_contract_address]

# Fibrous交换路径
swap = [{
    "token_in": Contracts.usdt_contract_address,
    "token_out": Contracts.eth_contract_address,
    "rate": 1000000,
    "protocol": 2,
    "pool_address": 0x45e7131d776dddc137e30bdd490b431c7144677e97bf9369f629ed8d3fb7dd6  # JediSwap: ETH/USDT Pool

}]
params = {
    "token_in": Contracts.usdt_contract_address,
    "token_out": Contracts.eth_contract_address,
    "amount": 1000000,
    "min_received": 0,
    "destination": Accounts.account1["Address"]
}


async def starknet_run():
    # 批准所有合约使用USDT代币
    sithswap_usdt_approval = usdt_contract.functions["approve"].prepare(
        spender=Contracts.sithswap_contract_address,
        amount=usdt_amount
    )
    myswap_usdt_approval = usdt_contract.functions["approve"].prepare(
        spender=Contracts.myswap_contract_address,
        amount=usdt_amount
    )
    tenkswap_usdt_approval = usdt_contract.functions["approve"].prepare(
        spender=Contracts.tenkswap_contract_address,
        amount=usdt_amount
    )
    jediswap_usdt_approval = usdt_contract.functions["approve"].prepare(
        spender=Contracts.jediswap_contract_address,
        amount=usdt_amount
    )
    fibrous_usdt_approval = usdt_contract.functions["approve"].prepare(
        spender=Contracts.fibrous_contract_address,
        amount=usdt_amount
    )
    starkex_usdt_approval = usdt_contract.functions["approve"].prepare(
        spender=Contracts.starkex_contract_address,
        amount=usdt_amount
    )
    protoss_usdt_approval = usdt_contract.functions["approve"].prepare(
        spender=Contracts.protoss_contract_address,
        amount=usdt_amount
    )

    # 将USDT代币转为ETH代币并转给接收者(account1)
    # SithSwap
    sithswap_transaction = sithswap_contract.functions["swapExactTokensForTokensSimple"].prepare(
        amount_in=usdt_amount,
        amount_out_min=0,
        token_from=usdt_contract_address,
        token_to=eth_contract_address,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )
    # MySwap
    myswap_transaction = myswap_contract.functions["swap"].prepare(
        pool_id=4,  # ETH<->USDT池
        token_from_addr=Contracts.usdt_contract_address,
        amount_from=usdt_amount,
        amount_to_min=0
    )
    # JediSwap
    jediswap_transaction = jediswap_contract.functions["swap_exact_tokens_for_tokens"].prepare(
        amountIn=usdt_amount,
        amountOutMin=0,
        path=path,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )
    # 10kSwap
    tenkswap_transaction = tenkswap_contract.functions["swapExactTokensForTokens"].prepare(
        amountIn=usdt_amount,
        amountOutMin=0,
        path=path,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )
    # FibrousSwap
    fibrous_transaction = fibrous_contract.functions["swap"].prepare(
        swaps=swap,
        params=params
    )
    # StarkexSwap
    starkex_transaction = starkex_contract.functions["swapExactTokensForTokens"].prepare(
        amountIn=usdt_amount,
        amountOutMin=0,
        path=path,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )
    # ProtossSwap
    protoss_transaction = protoss_contract.functions["swapExactTokensForTokens"].prepare(
        amountIn=usdt_amount,
        amountOutMin=0,
        path=path,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )

    # 计算执行合约所需要的大概金额
    transaction = await Accounts.main_account1.sign_invoke_transaction(
        calls=[sithswap_usdt_approval, sithswap_transaction,
               myswap_usdt_approval, myswap_transaction,
               jediswap_usdt_approval, jediswap_transaction,
               tenkswap_usdt_approval, tenkswap_transaction,
               fibrous_usdt_approval, fibrous_transaction,
               starkex_usdt_approval, starkex_transaction,
               protoss_usdt_approval, protoss_transaction
               ],
        max_fee=0
    )
    estimate = await Accounts.main_account1.client.estimate_fee(transaction)
    gas_fee = estimate.overall_fee * 10 ** -18
    print(f"预计费用: {gas_fee} ETH")
    time.sleep(3)

    # # 开始执行所有合约
    # print('正在执行所有合约...')
    # invocation = await Accounts.main_account1.execute(
    #     [sithswap_usdt_approval, sithswap_transaction,
    #      myswap_usdt_approval, myswap_transaction,
    #      jediswap_usdt_approval, jediswap_transaction,
    #      tenkswap_usdt_approval, tenkswap_transaction,
    #      fibrous_usdt_approval, fibrous_transaction,
    #      starkex_usdt_approval, starkex_transaction,
    #      protoss_usdt_approval, protoss_transaction,
    #      ],
    #     max_fee=int(0.001 * 10 ** 18)
    # )
    # print('交易哈希为: ' + Web3.to_hex(invocation.transaction_hash))

asyncio.run(starknet_run())
