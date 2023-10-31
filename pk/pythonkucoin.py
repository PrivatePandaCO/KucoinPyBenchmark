from kucoin.client import Client # python-kucoin
import time

kc = Client("...", "...", "...")
send_time = time.time() * 1000

# DirtyOneliners
print(f"Order Latency: {round(kc.get_order(kc.create_market_order('DOGE-USDT', side=kc.SIDE_BUY, funds=0.1)['orderId'])['createdAt']- send_time, 9)} ms")
