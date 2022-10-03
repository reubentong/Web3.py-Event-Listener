from web3 import Web3
from concurrent.futures import ThreadPoolExecutor


class EventListener(object):
    def __init__(self, contract_address, rpc_url, abi, topic, event_hash):
        self.executor = ThreadPoolExecutor(max_workers=10)
        provider = Web3.HTTPProvider(rpc_url)
        self.w3 = Web3(provider)
        self.topic = topic
        self.hash = event_hash
        self.ca = contract_address
        self.last_block = self.w3.eth.blockNumber
        if abi:
            with open(abi, 'r') as a:
                self.abi = a.read()
            self.contract = self.w3.eth.contract(address=self.ca, abi=self.abi)

    def get_transactions(self):
        try:
            end = self.w3.eth.blockNumber
            if self.last_block >= end:
                return []
            start = self.last_block + 1
            event_filter = self.w3.eth.filter({
                "fromBlock": start,  # 14429861,
                "toBlock": end,  # 14429862,
                "address": self.ca,
                "topics": [self.topic]
            })
            data = event_filter.get_all_entries()
            print(data)
            self.last_block = end
            return data
        except:
            print('error has occurred')
            return []


def wallet_truncate(address):
    first_part = address[0:5]
    last_part = address[38:42]
    truncated = first_part + "..." + last_part
    return truncated
