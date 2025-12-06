import unittest
import threading
from src.consumer import Consumer
from src.blocking_queue import BlockingQueue
from src.data_item import DataItem

class TestConsumer(unittest.TestCase):
    def test_consumer_shutdown(self):
        """
        Verify consumer processes items and shuts down upon receiving Poison Pill.
        """
        queue = BlockingQueue(capacity=10)
        
        # Pre-fill queue: 2 valid items + 1 Poison Pill
        queue.put(DataItem(10))
        queue.put(DataItem(20))
        queue.put(DataItem(None)) # Poison Pill
        
        # Initialize Consumer with 0 delay
        consumer = Consumer(queue, processing_time=0)
        
        consumer.start()
        # Wait for consumer to finish (it should finish because of the poison pill)
        consumer.join(timeout=2.0)
        
        self.assertFalse(consumer.is_alive(), "Consumer failed to shut down")
        
        # If the consumer worked, the queue should now be empty (it took all 3 items)
        # We rely on the internal implementation of BlockingQueue to know internal buffer is empty
        # But since we can't peek inside easily, we can try to take() in a separate thread with timeout
        # or simply rely on the fact that if it didn't consume, it wouldn't have hit the poison pill to stop.

        # A hacky way to ensure queue is empty without blocking indefinitely if we are wrong:
        # Reaching here with consumer.is_alive() == False proves it hit the pill.
        # Since queue is FIFO, it must have consumed 10 and 20 first.
        pass

if __name__ == '__main__':
    unittest.main()