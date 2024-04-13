import time
from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract
from Info import SingleAccount
from Info.Contracts import jediswap_contract_abi, jediswap_contract_address, eth_contract_address, eth_contract_abi, \
    usdt_contract_address, usdt_contract_abi

# JediSwap合约以及合约使用者
jediswap_contract = Contract(provider=Accounts.main_account1, address=jediswap_contract_address,
                             abi=json.loads(jediswap_contract_abi))
# 代币合约
eth_contract = Contract(provider=Accounts.main_account1, address=eth_contract_address,
                        abi=json.loads(eth_contract_abi))
usdt_contract = Contract(provider=Accounts.main_account1, address=usdt_contract_address,
                        abi=json.loads(usdt_contract_abi))

# 交换路径
path = [Contracts.usdt_contract_address, Contracts.eth_contract_address]

# 将要交易的eth数量
eth_amount = int(0.0001 * 10 ** 18)
# 将要交易的usdt数量
usdt_amount = int(1 * 10 ** 6)


# 交换代币函数
async def jedi_swap():
    usdt_contract = Contracts.usdt_contract
    # 批准合约使用USDT代币
    usdt_approval = usdt_contract.functions["approve"].prepare(
        Contracts.jediswap_contract_address,
        usdt_amount,
        max_fee=int(0.0004 * 10 ** 18)
    )
    # 确定交易后能获得的代币
    amounts_out = await jediswap_contract.functions['get_amounts_out'].call(amountIn=usdt_amount, path=path)
    print(amounts_out)
    # 将USDT代币转为ETH代币并转给接收者(account1)
    transaction = jediswap_contract.functions["swap_exact_tokens_for_tokens"].prepare(
        amountIn=usdt_amount,
        amountOutMin=0,
        path=path,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60),
        max_fee=int(0.0004 * 10 ** 18)
    )

    print('JediSwap开始进行交换代币:')
    invocation = await Accounts.main_account1.execute([usdt_approval, transaction], max_fee=int(0.0004 * 10 ** 18))
    print('Swap Hash: ' + Web3.to_hex(invocation.transaction_hash))


# 添加流动性函数 ETH & USDT
async def add_liquidity():
    # 批准合约使用ETH代币
    eth_approval = eth_contract.functions["approve"].prepare(
        Contracts.jediswap_contract_address,
        eth_amount,
        max_fee=int(0.0001 * 10 ** 18)
    )
    usdt_contract = Contracts.usdt_contract
    # 批准合约使用ETH代币
    usdt_approval = usdt_contract.functions["approve"].prepare(
        Contracts.jediswap_contract_address,
        usdt_amount,
        max_fee=int(0.0001 * 10 ** 18)
    )
    # 一定数量ETH转USDT的数量
    usdt_amounts_out = await jediswap_contract.functions['get_amounts_out'].call(amountIn=eth_amount,
                                                                                           path=path)
    print(usdt_amounts_out)
    usdt_amounts_out = usdt_amounts_out.as_dict()['amounts'][1]
    print(usdt_amounts_out)
    # 设置滑点
    slippage = 0.01
    # ETH最小数量
    eth_amount_out_min = int(int(eth_amount) * (1 - slippage))
    # USDT最小数量
    usdt_amount_out_min = int(int(usdt_amounts_out) * (1 - slippage))
    # 添加流动性
    liquidity = jediswap_contract.functions["add_liquidity"].prepare(
        tokenA=Contracts.eth_contract_address,
        tokenB=Contracts.usdt_contract_address,
        amountADesired=eth_amount,  # 代币ETH的数量
        amountBDesired=usdt_amounts_out,  # 代币USDT的数量
        amountAMin=0,  # 代币ETH的最小数量
        amountBMin=0,  # 代币USDT的最小数量
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )
    print('开始添加流动性:')
    invocation = await Accounts.main_account1.execute([eth_approval,usdt_approval,liquidity], max_fee=int(0.0004 * 10 ** 18))
    print('Add Liquidity Hash: ' + Web3.to_hex(invocation.transaction_hash))


# 移除流动性函数
async def remove_liquidity():
    # 批准合约使用ETH代币
    eth_approval = eth_contract.functions["approve"].prepare(
        Contracts.jediswap_contract_address,
        eth_amount,
        max_fee=int(0.0001 * 10 ** 18)
    )
    usdt_contract = Contracts.usdt_contract
    # 批准合约使用ETH代币
    usdt_approval = usdt_contract.functions["approve"].prepare(
        Contracts.jediswap_contract_address,
        usdt_amount,
        max_fee=int(0.0001 * 10 ** 18)
    )
    liquidity = jediswap_contract.functions["remove_liquidity"].prepare(
        tokenA=Contracts.eth_contract_address,
        tokenB=Contracts.usdt_contract_address,
        liquidity=int(0.00000000310026516 * 10 ** 18),
        amountAMin=0,
        amountBMin=0,
        to=Accounts.account1["Address"],
        deadline=int(time.time() + 60 * 60)
    )
    print('开始移除流动性:')
    invocation = await Accounts.main_account1.execute([eth_approval,usdt_approval,liquidity], max_fee=int(0.0004 * 10 ** 18))
    print('Remove Liquidity Hash: ' + Web3.to_hex(invocation.transaction_hash))


# asyncio.run(jedi_swap())