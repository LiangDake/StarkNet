from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair, StarkCurveSigner

# Creates an instance of account which is already deployed
# Account using transaction version=1 (has __validate__ function)
client = FullNodeClient(node_url="your.node.url")
account = Account(
    client=client,
    address="0x4321",
    key_pair = KeyPair.from_private_key(key=123),
    chain=StarknetChainId.TESTNET,
)


# Instead of providing key_pair it is possible to specify a signer
signer = StarkCurveSigner("0x1234", key_pair, StarknetChainId.TESTNET)

account = Account(client=client, address="0x1234", signer=signer)