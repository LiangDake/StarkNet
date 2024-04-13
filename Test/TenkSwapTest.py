import time
from web3 import Web3
import asyncio
import Accounts
import Contracts
import TestContracts


# 批准函数
async def approve():
    # 账户1(测试网)
    test_account1 = Accounts.test_account1
    # 交换路径
    path = [Contracts.eth_contract_address, Contracts.dai_contract_address]
    eth_contract = TestContracts.eth_contract
    contract = TestContracts.tenkswap_contract
    # 批准合约使用ETH代币
    approve = eth_contract.functions["approve"].prepare(
        Contracts.tenkswap_contract_address,
        100000000000000
    )

    # 将ETH代币转为DAI代币再换成USDC代币并转给接收者(account2)
    transaction = contract.functions["swapExactTokensForTokens"].prepare(
        amountIn=100000000000,
        amountOutMin=0,
        path=path,
        to=Accounts.account1['Address'],
        deadline=int(time.time() + 60 * 60)
    )

    print('开始进行swap')
    invocation = await test_account1.execute([approve, transaction], max_fee=int(1e15))
    print(Web3.to_hex(invocation.transaction_hash))
    time.sleep(2)

asyncio.run(approve())


