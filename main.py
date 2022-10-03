import asyncio

from global_scripts import event_listener
from global_scripts.event_listener import wallet_truncate

listen = event_listener.EventListener()


async def event_subscription():
    data = listen.get_transactions()
    if data:
        for tx in data:
            tx_input = tx['data']
            await asyncio.sleep(2)


async def main():
    while True:
        asyncio.ensure_future(event_subscription())
        await asyncio.sleep(0.1)


asyncio.run(main())
