import unittest
from src.models import CarSale
from src.analysis import functional_aggregate, get_max_entry

class TestFunctionalAnalysis(unittest.TestCase):
    def setUp(self):
        self.mock_stream = [
            CarSale(1, 100.0, "toyota", "camry", 2010, "clean", 5000, "black"),
            CarSale(2, 200.0, "toyota", "camry", 2010, "clean", 6000, "white"),
            CarSale(3, 1000.0, "bmw", "x5", 2020, "clean", 1000, "blue")
        ]

    def test_aggregation_logic(self):
        # We test the aggregator using explicit lambdas
        result = functional_aggregate(
            iter(self.mock_stream),
            key_selector=lambda c: c.full_name,
            value_mapper=lambda c: {'count': 1, 'revenue': c.price}
        )
        
        # Toyota Camry: 2 units, 300 revenue
        self.assertEqual(result["toyota camry"]['count'], 2)
        self.assertEqual(result["toyota camry"]['revenue'], 300.0)
        
        # BMW X5: 1 unit, 1000 revenue
        self.assertEqual(result["bmw x5"]['revenue'], 1000.0)

    def test_max_logic(self):
        data = {
            "cheap": {'count': 10, 'revenue': 100},
            "expensive": {'count': 1, 'revenue': 1000}
        }
        
        # Test max by count
        name, stats = get_max_entry(data, lambda x: x['count'])
        self.assertEqual(name, "cheap")
        
        # Test max by revenue
        name, stats = get_max_entry(data, lambda x: x['revenue'])
        self.assertEqual(name, "expensive")

if __name__ == '__main__':
    unittest.main()