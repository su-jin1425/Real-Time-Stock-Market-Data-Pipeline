import os
import json
from confluent_kafka import Consumer, KafkaError, KafkaException

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:29092")
TOPIC = "stock_ticks"

def main():
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'raw_logger_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([TOPIC])
    
    print(f"Starting consumer, listening to {KAFKA_BROKER} on topic {TOPIC}...")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f'{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}')
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                data = json.loads(msg.value().decode('utf-8'))
                print(f"Received tick: {data['stock_symbol']} at {data['price']} (Vol: {data['volume']})")
                
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

if __name__ == "__main__":
    main()
