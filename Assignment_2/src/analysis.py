from functools import reduce
from typing import Iterator, Dict, Callable, Any, TypeVar
from src.models import CarSale

# Generic type var to allow this to work with any object, not just Cars
T = TypeVar('T')

def functional_aggregate(
    stream: Iterator[T],
    key_selector: Callable[[T], str],
    value_mapper: Callable[[T], Dict[str, float]]
) -> Dict[str, Dict[str, float]]:
    """
    A generic Higher-Order Function for Map/Reduce.
    
    Args:
        stream: The data source.
        key_selector: Lambda to group data (e.g., lambda c: c.brand).
        value_mapper: Lambda to extract metrics (e.g., lambda c: {'count': 1, 'rev': c.price}).
    
    """
    
    def reducer(acc: Dict[str, Dict[str, float]], item: T) -> Dict[str, Dict[str, float]]:
        # Calculate key/values for the current item
        key = key_selector(item)
        values = value_mapper(item)
        
        # Get existing state or initialize defaults
        current = acc.get(key, {'count': 0.0, 'revenue': 0.0})
        
        # Aggregate logic
        acc[key] = {
            'count': current['count'] + values.get('count', 0),
            'revenue': current['revenue'] + values.get('revenue', 0.0)
        }
        return acc

    # Reduce the entire stream into a single dictionary
    return reduce(reducer, stream, {})

def get_max_entry(
    data: Dict[str, Dict[str, float]], 
    comparator: Callable[[dict], float]
) -> tuple:
    
    # Finds the maximum entry based on a Lambda comparator.
    if not data:
        return ("None", {'count': 0, 'revenue': 0.0})
    
    return max(data.items(), key=lambda item: comparator(item[1]))