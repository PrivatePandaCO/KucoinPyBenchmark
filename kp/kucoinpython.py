from kucoin.client import Trade
import time

client = Trade("...", "...", "...")

send_time = time.time() * 1000
print(f"Order Latency: {round(client.get_order_details(client.create_market_order('DOGE-USDT', 'buy', funds=0.1)['orderId'])['createdAt'] - send_time, 9)} ms")
