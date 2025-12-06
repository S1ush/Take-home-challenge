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
        for i in range(1, self.item_count + 1):
            item = DataItem(i)
            logger.info(f"Producing: {item}")
            self.queue.put(item)
            time.sleep(self.delay)
        
        # Send Poison Pill (Shutdown Signal)
        logger.info("Producer finished. Sending Poison Pill.")
        self.queue.put(DataItem(None))