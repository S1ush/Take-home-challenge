import unittest
import threading
import time
from src.blocking_queue import BlockingQueue
from src.data_item import DataItem

class TestBlockingQueue(unittest.TestCase):
    def setUp(self):
        self.queue = BlockingQueue(capacity=2)

    def test_fifo_order(self):
        """Test that items are retrieved in the order they were added."""
        self.queue.put(DataItem(1))
        self.queue.put(DataItem(2))
        
        self.assertEqual(self.queue.take().payload, 1)
        self.assertEqual(self.queue.take().payload, 2)

    def test_blocking_on_empty(self):
        """Test that take() blocks when the queue is empty."""
        # Helper to put item after a delay
        def delayed_put():
            time.sleep(0.1)
            self.queue.put(DataItem(99))

        t = threading.Thread(target=delayed_put)
        t.start()
        
        start_time = time.time()
        # This should block until the thread puts the item
        item = self.queue.take()
        end_time = time.time()
        
        t.join()
        
        self.assertEqual(item.payload, 99)
        # Ensure it actually waited roughly 0.1s
        self.assertGreaterEqual(end_time - start_time, 0.1)

    def test_blocking_on_full(self):
        """Test that put() blocks when the queue is full."""
        # Fill the queue to capacity (2 items)
        self.queue.put(DataItem(1))
        self.queue.put(DataItem(2))

        # Helper to remove item after a delay to free space
        def delayed_take():
            time.sleep(0.1)
            self.queue.take()

        t = threading.Thread(target=delayed_take)
        t.start()

        start_time = time.time()
        # This should block until delayed_take() runs
        self.queue.put(DataItem(3)) 
        end_time = time.time()

        t.join()

        # The queue should now contain [2, 3] (1 was removed)
        self.assertEqual(self.queue.take().payload, 2)
        self.assertEqual(self.queue.take().payload, 3)
        self.assertGreaterEqual(end_time - start_time, 0.1)

if __name__ == '__main__':
    unittest.main()