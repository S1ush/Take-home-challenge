import unittest
from src.data_item import DataItem

class TestDataItem(unittest.TestCase):
    def test_initialization(self):
        """Test that DataItem initializes with correct payload."""
        item = DataItem(123)
        self.assertEqual(item.payload, 123)
        self.assertEqual(str(item), "DataItem(payload=123)")

    def test_poison_pill_check_true(self):
        """Test that a None payload is correctly identified as a poison pill."""
        item = DataItem(None)
        self.assertTrue(item.is_poison_pill())

    def test_poison_pill_check_false(self):
        """Test that a valid payload is NOT identified as a poison pill."""
        item = DataItem("Valid Data")
        self.assertFalse(item.is_poison_pill())

if __name__ == '__main__':
    unittest.main()