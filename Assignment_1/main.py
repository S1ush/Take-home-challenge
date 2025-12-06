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
    try:
        # Configuration

        # Define the maximum number of items the queue can hold at once
        QUEUE_CAPACITY = 3
        # Define the total number of items the producer needs to generate
        TOTAL_ITEMS = 10
        
        # Initialization
        # Create the thread-safe shared queue
        shared_queue = BlockingQueue(QUEUE_CAPACITY)
        
        producer = Producer(queue=shared_queue, item_count=TOTAL_ITEMS, delay=0.05)
        consumer = Consumer(queue=shared_queue, processing_time=0.1)

        # Start Threads
        # Begin the execution of the Producer and Consumer threads concurrently
        producer.start()
        consumer.start()

        # Wait for completion
        # Block the main thread until both the Producer and Consumer threads have finished execution
        producer.join()
        consumer.join()

        logging.info("All tasks completed successfully.")

    except KeyboardInterrupt:
        logging.warning("Application interrupted by user.")
    except Exception as e:
        logging.error(f"Application failed with error: {e}")

if __name__ == "__main__":
    main()