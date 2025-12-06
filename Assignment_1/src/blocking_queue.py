import threading
import logging
from typing import List
from .data_item import DataItem

logger = logging.getLogger(__name__)

class BlockingQueue:

    # thread-safe bounded buffer implementing the Producer-Consumer pattern.
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Queue capacity must be positive")
        
        self._buffer: List[DataItem] = []
        self._capacity = capacity
        self._cv = threading.Condition()

    def put(self, item: DataItem) -> None:
        
       
        # Inserts an item into the queue. Blocks if the queue is full. 
        try:
            with self._cv:

                # A while loop is used instead of an if statement to handle wakeups
                while len(self._buffer) == self._capacity:
                    logger.debug("Queue full. Producer waiting...")

                    #Release the lock and wait until notified by the Consumer
                    self._cv.wait()
                
                # Once space is available, add the item to the buffer
                self._buffer.append(item)
                logger.debug(f"Item added: {item}")

                # Notify all waiting threads
                self._cv.notify_all()

        except RuntimeError as e:
            logger.error(f"Critical error in Queue put operation: {e}")
            raise

    def take(self) -> DataItem:
        
        #Removes an item from the queue. Blocks if the queue is empty.
        try:
            with self._cv:

                # Wait while there is no data to consume.
                while len(self._buffer) == 0:
                    logger.debug("Queue empty. Consumer waiting...")

                    # Release the lock and wait until notified by the Producer
                    self._cv.wait()
                
                item = self._buffer.pop(0)
                logger.debug(f"Item removed: {item}")
                # Notify all waiting threads 
                self._cv.notify_all()
                return item
        except RuntimeError as e:
            logger.error(f"Critical error in Queue take operation: {e}")
            raise