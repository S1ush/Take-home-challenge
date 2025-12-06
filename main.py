import logging
import sys
from src.blocking_queue import BlockingQueue
from src.producer import Producer
from src.consumer import Consumer

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(threadName)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    # Configuration
    QUEUE_CAPACITY = 3
    TOTAL_ITEMS = 10
    
    # Initialization
    shared_queue = BlockingQueue(QUEUE_CAPACITY)
    
    producer = Producer(queue=shared_queue, item_count=TOTAL_ITEMS, delay=0.05)
    consumer = Consumer(queue=shared_queue, processing_time=0.1)

    # Start Threads
    producer.start()
    consumer.start()

    # Wait for completion
    producer.join()
    consumer.join()

    logging.info("All tasks completed successfully.")

if __name__ == "__main__":
    main()