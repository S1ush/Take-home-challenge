import unittest
from unittest.mock import patch, mock_open
from src.models import CarSale
from src.streams import car_sales_stream
from src.analysis import functional_aggregate, get_max_entry

class TestCarSalesProject(unittest.TestCase):

    # 1.Model Test
    def test_model_creation_and_property(self):
        """Test that the data class holds data and full_name property works."""
        car = CarSale(0, 5000.0, "ford", "mustang", 2020, "clean", 1000.0, "red")
        
        self.assertEqual(car.brand, "ford")
        self.assertEqual(car.price, 5000.0)
        # Check the computed property
        self.assertEqual(car.full_name, "ford mustang")


    # 2. STREAM TESTS (Data Loader)  
    def test_stream_valid_data(self):
        """Test reading a valid CSV line converts to CarSale object."""
        csv_data = (
            "id,price,brand,model,year,title_status,mileage,color\n"
            "1,2000,toyota,camry,2010,clean,5000,black\n"
        )
        
        with patch("builtins.open", mock_open(read_data=csv_data)):
            # We mock the file, so 'dummy.csv' doesn't need to exist
            stream = car_sales_stream("dummy.csv")
            results = list(stream)
            
            self.assertEqual(len(results), 1)
            self.assertIsInstance(results[0], CarSale)
            self.assertEqual(results[0].price, 2000.0)
            self.assertEqual(results[0].model, "camry")

    def test_stream_malformed_data(self):
        """Test that rows with bad numbers (e.g., text in price) are skipped."""
        csv_data = (
            "id,price,brand,model,year,title_status,mileage,color\n"
            "1,INVALID,toyota,camry,2010,clean,5000,black\n"  # Bad Price
            "2,3000,honda,civic,2012,clean,6000,red\n"         # Good Row
        )

        with patch("builtins.open", mock_open(read_data=csv_data)):
            stream = car_sales_stream("dummy.csv")
            results = list(stream)

            # Should skip the first row, parse the second
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].brand, "honda")



    # 3. ANALYSIS TESTS (Functional Logic)
    def setUp(self):
        """Setup mock data for analysis tests."""
        self.mock_data = [
            CarSale(1, 100.0, "brandA", "model1", 2020, "clean", 100, "red"),
            CarSale(2, 200.0, "brandA", "model1", 2020, "clean", 100, "blue"),
            CarSale(3, 500.0, "brandB", "model2", 2020, "clean", 100, "white"),
        ]

    def test_functional_aggregate_logic(self):
        """Test if group by and sum logic works correctly."""
        result = functional_aggregate(
            iter(self.mock_data),
            key_selector=lambda c: c.full_name,
            value_mapper=lambda c: {'count': 1, 'revenue': c.price}
        )

        # brandA model1: 2 items, 100 + 200 = 300 revenue
        self.assertEqual(result["brandA model1"]["count"], 2)
        self.assertEqual(result["brandA model1"]["revenue"], 300.0)

        # brandB model2: 1 item, 500 revenue
        self.assertEqual(result["brandB model2"]["count"], 1)
        self.assertEqual(result["brandB model2"]["revenue"], 500.0)

    def test_aggregate_empty_stream(self):
        """Test aggregation on empty input."""
        result = functional_aggregate(
            iter([]),
            key_selector=lambda c: c.brand,
            value_mapper=lambda c: {}
        )
        self.assertEqual(result, {})

    def test_get_max_entry_logic(self):
        """Test finding the max entry based on custom comparators."""
        data_map = {
            "ItemA": {'count': 10, 'revenue': 100.0},
            "ItemB": {'count': 1, 'revenue': 1000.0}
        }

        # Case A: Max by Count (ItemA should win)
        name, stats = get_max_entry(data_map, lambda x: x['count'])
        self.assertEqual(name, "ItemA")
        self.assertEqual(stats['count'], 10)

        # Case B: Max by Revenue (ItemB should win)
        name, stats = get_max_entry(data_map, lambda x: x['revenue'])
        self.assertEqual(name, "ItemB")
        self.assertEqual(stats['revenue'], 1000.0)

    def test_get_max_entry_empty(self):
        """Test getting max from empty dictionary returns safe defaults."""
        name, stats = get_max_entry({}, lambda x: x['count'])
        self.assertEqual(name, "None")
        self.assertEqual(stats['count'], 0)
        self.assertEqual(stats['revenue'], 0.0)

if __name__ == '__main__':
    unittest.main()