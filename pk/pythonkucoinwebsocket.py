import asyncio
import time

from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager

async def main():
    global loop

    latency = []

    # callback function that receives messages from the socket
    async def handle_evt(msg):
        if msg['topic'] == '/market/level2:BTC-USDT':
            latency.append(time.time() * 1000 - msg["data"]["time"])

    client = Client("...", "...", "...")
    ksm = await KucoinSocketManager.create(loop, client, handle_evt)
    await ksm.subscribe('/market/level2:BTC-USDT')

    await asyncio.sleep(5)

    print(f"""
Minimum Websocket Latency: {round(min(latency), 9)} ms
Average Websocket Latency: {round(sum(latency)/len(latency), 9)} ms
    """)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
