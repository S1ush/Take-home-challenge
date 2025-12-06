import unittest
from src.blocking_queue import BlockingQueue
from src.producer import Producer
from src.consumer import Consumer

class TestIntegration(unittest.TestCase):
    def test_full_cycle(self):
        """
        Runs the actual Producer and Consumer threads and ensures 
        deadlocks do not occur and clean shutdown happens.
        """
        queue = BlockingQueue(capacity=2)
        item_count = 5
        
        # Create threads with minimal delays for fast testing
        producer = Producer(queue, item_count, delay=0.01)
        consumer = Consumer(queue, processing_time=0.01)
        
        producer.start()
        consumer.start()
        
        # Set a timeout for join to detect deadlocks
        producer.join(timeout=2)
        consumer.join(timeout=2)
        
        # Verify threads are not alive (meaning they shut down correctly)
        self.assertFalse(producer.is_alive(), "Producer failed to shut down")
        self.assertFalse(consumer.is_alive(), "Consumer failed to shut down")

if __name__ == '__main__':
    unittest.main()