from starknet_py.net.full_node_client import FullNodeClient


# 节点API
test_node_url = "https://starknet-testnet.blastapi.io/f281ef1e-7c99-440c-817f-7c113222e847"
main_node_url = "https://starknet-mainnet.blastapi.io/f281ef1e-7c99-440c-817f-7c113222e847"

test_client = FullNodeClient(test_node_url)
main_client = FullNodeClient(main_node_url)

# 地址数组和私钥数组
address = []
private_key = []

# 钱包账号
wallet_accounts = [
    {
        "mnemonic": "pepper awful tomorrow oppose theme demise stumble patrol baby pioneer wild liar",
        "privateKey": "0x0745c4c0e04862ed40517ccf8d57c53ba0645734725ac38c6897318bfa67a690",
        "publicKey": "0x6e1daffb1a833dafb6edac36ce59ca41209cda85d6a66fe40146934ab9196b0",
        "address": "0x04129694b4825c92b21e2111e5049a1706634de04a854518fddab97b4efef9fb"
    },
    {
        "mnemonic": "pyramid pave atom duck february chapter bridge gossip identify usual ancient bicycle",
        "privateKey": "0x0622f6866d9d5b0900427ffa14b37c3dbd59c476978107b8a93b94c46a8576bb",
        "publicKey": "0x4e746c9876f9da697a906d7c5b02e5e6d4d64629e8f0bab0bb7219035ca3ba6",
        "address": "0x0577aedbf88cdf70c13b00044fff987278ad9bd7c282f6e5a816713394414ddd"
    },
    {
        "mnemonic": "turkey example menu lend more remove own bless evolve vicious skin inspire",
        "privateKey": "0x0696b8c2bbfaf27a5c0c1c3c5c11df768fe51122ef28c744b94d09db44ea83ac",
        "publicKey": "0x46df983ef9cc2f32a6841625f4606df305f324551f59dc574b4c1d22d1f0d9f",
        "address": "0x07e3f1e0ad9feab31a36d06e2fe1de575aaf5af144b8f764c4919ce0be056270"
    }
]

# 获取钱包地址
for i in wallet_accounts:
    # 将钱包地址导入address数组
    address.append(i["address"])

# 获取钱包私钥
for i in wallet_accounts:
    # 将私钥导入private_key数组
    private_key.append(i["privateKey"])
