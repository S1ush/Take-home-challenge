import unittest
from src.producer import Producer
from src.blocking_queue import BlockingQueue

class TestProducer(unittest.TestCase):
    def test_producer_logic(self):
        """
        Verify producer adds exactly N items followed by a Poison Pill.
        """
        # Create a queue large enough so the producer never blocks during this test
        queue = BlockingQueue(capacity=10)
        item_count = 3
        
        # Initialize Producer with 0 delay for fast testing
        producer = Producer(queue, item_count, delay=0)
        
        producer.start()
        producer.join()

        # Verify contents
        # Expecting: 1, 2, 3, None (Poison Pill)
        self.assertEqual(queue.take().payload, 1)
        self.assertEqual(queue.take().payload, 2)
        self.assertEqual(queue.take().payload, 3)
        
        # Verify the last item is the Poison Pill
        last_item = queue.take()
        self.assertTrue(last_item.is_poison_pill())

if __name__ == '__main__':
    unittest.main()