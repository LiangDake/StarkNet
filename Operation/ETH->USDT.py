import time
from web3 import Web3
import asyncio
from Info import Contracts
import json
from starknet_py.contract import Contract

from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

from Info.AllAccounts import address, private_key, main_client
from Info.Contracts import (eth_contract_address, eth_contract_abi,
                            sithswap_contract_address, sithswap_contract_abi,
                            myswap_contract_address, myswap_contract_abi,
                            jediswap_contract_address, jediswap_contract_abi,
                            fibrous_contract_address, fibrous_contract_abi,
                            tenkswap_contract_address, tenkswap_contract_abi,
                            protoss_contract_address, protoss_contract_abi,
                            starkex_contract_address, starkex_contract_abi, usdt_contract_address
                            )


async def starknet_run():
    for i in range(0, 1):
        main_account = Account(
            client=main_client,
            address=int(address[i], 16),
            key_pair=KeyPair.from_private_key(private_key[i]),
            chain=StarknetChainId.MAINNET,
        )
        # SithSwap合约以及合约使用者
        sithswap_contract = Contract(provider=main_account, address=sithswap_contract_address,
                                     abi=json.loads(sithswap_contract_abi))
        # MySwap合约以及合约使用者
        myswap_contract = Contract(provider=main_account, address=myswap_contract_address,
                                   abi=json.loads(myswap_contract_abi))
        # JediSwap合约以及合约使用者
        jediswap_contract = Contract(provider=main_account, address=jediswap_contract_address,
                                     abi=json.loads(jediswap_contract_abi))
        # 10kSwap合约以及合约使用者
        tenkswap_contract = Contract(provider=main_account, address=tenkswap_contract_address,
                                     abi=json.loads(tenkswap_contract_abi))
        # Fibrous合约以及合约使用者
        fibrous_contract = Contract(provider=main_account, address=fibrous_contract_address,
                                    abi=json.loads(fibrous_contract_abi))
        # starkex合约以及合约使用者
        starkex_contract = Contract(provider=main_account, address=starkex_contract_address,
                                    abi=json.loads(starkex_contract_abi))
        # protoss合约以及合约使用者
        protoss_contract = Contract(provider=main_account, address=protoss_contract_address,
                                    abi=json.loads(protoss_contract_abi))

        # ETH合约以及每一笔交易的ETH代币数
        eth_contract = Contract(provider=main_account, address=eth_contract_address,
                                 abi=json.loads(eth_contract_abi))
        eth_amount = int(1 * 10 ** 14)

        # Fibrous交换路径
        swap = [{
            "token_in": Contracts.eth_contract_address,
            "token_out": Contracts.usdt_contract_address,
            "rate": 1000000,
            "protocol": 2,
            "pool_address": 0x45e7131d776dddc137e30bdd490b431c7144677e97bf9369f629ed8d3fb7dd6  # ETH/USDT Pool
        }]
        params = {
            "token_in": Contracts.eth_contract_address,
            "token_out": Contracts.usdt_contract_address,
            "amount": 10000000000000,
            "min_received": 0,
            "destination": int(address[i], 16)
        }
        # JediSwap交换路径
        path = [Contracts.eth_contract_address, Contracts.usdt_contract_address]

        # 批准所有合约使用USDT代币
        sithswap_eth_approval = eth_contract.functions["approve"].prepare(
            spender=Contracts.sithswap_contract_address,
            amount=eth_amount
        )
        myswap_eth_approval = eth_contract.functions["approve"].prepare(
            spender=Contracts.myswap_contract_address,
            amount=eth_amount
        )
        tenkswap_eth_approval = eth_contract.functions["approve"].prepare(
            spender=Contracts.tenkswap_contract_address,
            amount=eth_amount
        )
        jediswap_eth_approval = eth_contract.functions["approve"].prepare(
            spender=Contracts.jediswap_contract_address,
            amount=eth_amount
        )
        fibrous_eth_approval = eth_contract.functions["approve"].prepare(
            spender=Contracts.fibrous_contract_address,
            amount=eth_amount
        )
        starkex_eth_approval = eth_contract.functions["approve"].prepare(
            spender=Contracts.starkex_contract_address,
            amount=eth_amount
        )
        protoss_eth_approval = eth_contract.functions["approve"].prepare(
            spender=Contracts.protoss_contract_address,
            amount=eth_amount
        )

        # 将ETH代币转为USDT代币并转给接收者(account)
        # SithSwap
        sithswap_transaction = sithswap_contract.functions["swapExactTokensForTokensSimple"].prepare(
            amount_in=eth_amount,
            amount_out_min=0,
            token_from=eth_contract_address,
            token_to=usdt_contract_address,
            to=int(address[i], 16),
            deadline=int(time.time() + 60 * 60)
        )
        # MySwap
        myswap_transaction = myswap_contract.functions["swap"].prepare(
            pool_id=4,  # ETH<->USDT池
            token_from_addr=Contracts.eth_contract_address,
            amount_from=eth_amount,
            amount_to_min=0
        )
        # JediSwap
        jediswap_transaction = jediswap_contract.functions["swap_exact_tokens_for_tokens"].prepare(
            amountIn=eth_amount,
            amountOutMin=0,
            path=path,
            to=int(address[i], 16),
            deadline=int(time.time() + 60 * 60)
        )
        # 10kSwap
        tenkswap_transaction = tenkswap_contract.functions["swapExactTokensForTokens"].prepare(
            amountIn=eth_amount,
            amountOutMin=0,
            path=path,
            to=int(address[i], 16),
            deadline=int(time.time() + 60 * 60)
        )
        # FibrousSwap
        fibrous_transaction = fibrous_contract.functions["swap"].prepare(
            swaps=swap,
            params=params
        )
        # StarkexSwap
        starkex_transaction = starkex_contract.functions["swapExactTokensForTokens"].prepare(
            amountIn=eth_amount,
            amountOutMin=0,
            path=path,
            to=int(address[i], 16),
            deadline=int(time.time() + 60 * 60)
        )
        # ProtossSwap
        protoss_transaction = protoss_contract.functions["swapExactTokensForTokens"].prepare(
            amountIn=eth_amount,
            amountOutMin=0,
            path=path,
            to=int(address[i], 16),
            deadline=int(time.time() + 60 * 60)
        )

        # 将要使用的交换合约
        call = [
            sithswap_eth_approval, sithswap_transaction,
            myswap_eth_approval, myswap_transaction,
            jediswap_eth_approval, jediswap_transaction,
            tenkswap_eth_approval, tenkswap_transaction,
            fibrous_eth_approval, fibrous_transaction,
        ]

        # 计算执行合约所需要的大概金额
        transaction = await main_account.sign_invoke_transaction(
            calls=call,
            max_fee=0
        )
        estimate = await main_account.client.estimate_fee(transaction)
        gas_fee = estimate.overall_fee * 10 ** -18
        print(f"第{i+1}个钱包交易总预计费用: {gas_fee} ETH")
        # 开始执行所有合约
        print(f"第{i+1}个钱包正在执行所有合约...")
        invocation = await main_account.execute(
            calls=call,
            max_fee=int(0.001 * 10 ** 18)
        )
        print('它的交易哈希为: ' + Web3.to_hex(invocation.transaction_hash))
        time.sleep(2)
asyncio.run(starknet_run())
