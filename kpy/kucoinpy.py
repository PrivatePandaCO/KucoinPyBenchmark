from KucoinPy import KucoinPy as Kucoin
from KucoinPy import Order
from KucoinPy.http import Response
import random
from string import ascii_letters as asl
import time


class KucoinPyBenchmark:
    def __init__(self, api_key, api_secret, api_passphrase) -> None:
        self.ws_latency = []
        self.kc = Kucoin(api_key, api_secret, api_passphrase, defaults=[("/market/level2:BTC-USDT", False)], second_message_handler=self.msg_handler)

    def benchmark_order(self):
        cOid = "".join(random.choices(asl, k=10))
        send_time = time.time()*1000 # second to millisecond, measure time when we send request
        resp: Response = self.kc.order(
            Order(
                clientOid=cOid,
                side="sell",
                symbol="DOGE-USDT",
                type="market",
                size=8.6
            ),
            response=True
        )

        print(resp.raw_response)

        orderDetails = self.kc.get_order_details_with_clientOid(cOid, "DOGE-USDT", response=True)
        orderCreatedAt = orderDetails.json()['data']['createdAt'] # time when order was created on server

        return orderCreatedAt - send_time # time delta

    def msg_handler(self, data: dict):
        handle_time = time.time()*1000
        if "topic" not in data or data["topic"] != "/market/level2:BTC-USDT":
            return
        message_time = data["data"]["time"]

        self.ws_latency.append(handle_time - message_time)

    def benchmark_websocket(self):
        x = self.ws_latency.copy()
        return min(x), sum(x) / len(x)

    def benchmark_internal_websocket(self):
        # This was made possible by a minor change in the underlying library.
        # The modified version is now housed here: https://github.com/PrivatePandaCO/KucoinPy/tree/temp_benchmarking
        x = self.kc.internal_ws_benchmark.copy()
        return min(x), sum(x) / len(x)

bench = KucoinPyBenchmark("...", "...", "...")

order_bench = bench.benchmark_order()
time.sleep(5) # let latency cache build for accurate results
ws_bench = bench.benchmark_websocket()
internal_ws_bench = bench.benchmark_internal_websocket()

print(f"""
Summary:
Order Latency: {round(order_bench, 9)} ms

Minimum Internal Websocket Latency: {round(internal_ws_bench[0], 9)} ms
Average Internal Websocket Latency: {round(internal_ws_bench[1], 9)} ms


Minimum Websocket Latency: {round(ws_bench[0], 9)} ms
Average Websocket Latency: {round(ws_bench[1], 9)} ms

""")
