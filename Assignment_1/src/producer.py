import threading
import time
import logging
from .blocking_queue import BlockingQueue
from .data_item import DataItem

logger = logging.getLogger(__name__)

class Producer(threading.Thread):
    def __init__(self, queue: BlockingQueue, item_count: int, delay: float = 0.1):
        super().__init__()
        self.queue = queue
        self.item_count = item_count
        self.delay = delay

    def run(self):
        logger.info("Producer started.")
        try:
            # Loop from 1 up to the specific item_count
            for i in range(1, self.item_count + 1):
                item = DataItem(i)
                logger.info(f"Producing: {item}")

                # Insert the item into the shared queue.
                self.queue.put(item)

                # Sleep to simulate the time it takes to produce an item
                time.sleep(self.delay)
            
            # Send Poison Pill (Shutdown Signal)
            logger.info("Producer finished. Sending Poison Pill.")
            self.queue.put(DataItem(None))
            
        except Exception as e:
            logger.error(f"Producer encountered an unexpected error: {e}")