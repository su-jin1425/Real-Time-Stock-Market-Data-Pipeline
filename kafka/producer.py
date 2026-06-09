import os
import time
import json
import random
from datetime import datetime
from confluent_kafka import Producer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:29092")
TOPIC = "stock_ticks"

SYMBOLS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NFLX", "NVDA", "JPM", "V"]

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def generate_stock_tick():
    symbol = random.choice(SYMBOLS)
    base_price = {"AAPL": 150, "GOOGL": 2800, "MSFT": 300, "AMZN": 3400, "TSLA": 800, "META": 330, "NFLX": 600, "NVDA": 220, "JPM": 160, "V": 230}.get(symbol, 100)
    
    # Simulate random price movement
    price = round(base_price + random.uniform(-5.0, 5.0), 2)
    volume = random.randint(10, 1000)
    
    return {
        "stock_symbol": symbol,
        "price": price,
        "volume": volume,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def main():
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'client.id': 'python-producer'
    }
    
    producer = Producer(conf)
    print(f"Starting producer, connecting to {KAFKA_BROKER}...")
    
    try:
        while True:
            tick = generate_stock_tick()
            producer.produce(
                topic=TOPIC,
                key=tick["stock_symbol"].encode('utf-8'),
                value=json.dumps(tick).encode('utf-8'),
                callback=delivery_report
            )
            producer.poll(0)
            time.sleep(0.5)  # Simulate 2 ticks per second
            
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        producer.flush()

if __name__ == "__main__":
    main()
