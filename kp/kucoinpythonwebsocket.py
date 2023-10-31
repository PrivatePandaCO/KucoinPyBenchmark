import asyncio
import time

from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient


async def main():
    latency = []
    async def deal_msg(msg):
        if msg['topic'] == '/market/level2:BTC-USDT':
            latency.append(time.time() * 1000 - msg["data"]["time"])

    client = WsToken()
    ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False)

    await ws_client.subscribe('/market/level2:BTC-USDT')
    await asyncio.sleep(5)

    print(f"""
Minimum Websocket Latency: {round(min(latency), 9)} ms
Average Websocket Latency: {round(sum(latency)/len(latency), 9)} ms
    """)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
