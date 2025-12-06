import threading
import time
import logging
from .blocking_queue import BlockingQueue

logger = logging.getLogger(__name__)

class Consumer(threading.Thread):
    def __init__(self, queue: BlockingQueue, processing_time: float = 0.2):
        super().__init__()
        self.queue = queue
        self.processing_time = processing_time

    def run(self):
        logger.info("Consumer started.")
        try:
            while True:
                item = self.queue.take()

                if item.is_poison_pill():
                    logger.info("Poison Pill received. Shutting down Consumer.")
                    break

                logger.info(f"Consuming: {item.payload}")
                # Simulate processing time
                time.sleep(self.processing_time)
                
        except Exception as e:
            logger.error(f"Consumer encountered an unexpected error: {e}")