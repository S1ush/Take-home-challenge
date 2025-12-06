# Producer-Consumer Pattern Implementation

A thread-safe implementation of the classic Producer-Consumer pattern in Python, demonstrating concurrent programming concepts including thread synchronization, blocking queues, and wait/notify mechanisms.



## 🔍 Overview

This project implements a classic producer-consumer pattern where:
- A **Producer** thread generates data items and places them into a shared bounded buffer
- A **Consumer** thread retrieves and processes items from the shared buffer
- A **BlockingQueue** ensures thread-safe communication with automatic blocking when full or empty
- A **Poison Pill** pattern enables graceful shutdown of the consumer thread



## Requirements

- Python 3.7 or higher
- Standard library only (no external dependencies)

## Installation

1. **Clone the repository**
```bash
   git clone https://github.com/S1ush/Take-home-challenge.git

   cd Assignment_1/ 
```



## Usage

### Running the Application
```bash
python main.py
```

### Sample Output
```
2025-12-06 16:48:04,181 - [INFO] - Thread-1 - Producer started.
2025-12-06 16:48:04,181 - [INFO] - Thread-1 - Producing: DataItem(payload=1)
2025-12-06 16:48:04,181 - [INFO] - Thread-2 - Consumer started.
2025-12-06 16:48:04,181 - [INFO] - Thread-2 - Consuming: 1
2025-12-06 16:48:04,232 - [INFO] - Thread-1 - Producing: DataItem(payload=2)
2025-12-06 16:48:04,283 - [INFO] - Thread-2 - Consuming: 2
2025-12-06 16:48:04,283 - [INFO] - Thread-1 - Producing: DataItem(payload=3)
2025-12-06 16:48:04,334 - [INFO] - Thread-1 - Producing: DataItem(payload=4)
2025-12-06 16:48:04,383 - [INFO] - Thread-2 - Consuming: 3
2025-12-06 16:48:04,384 - [INFO] - Thread-1 - Producing: DataItem(payload=5)
2025-12-06 16:48:04,434 - [INFO] - Thread-1 - Producing: DataItem(payload=6)
2025-12-06 16:48:04,484 - [INFO] - Thread-2 - Consuming: 4
2025-12-06 16:48:04,485 - [INFO] - Thread-1 - Producing: DataItem(payload=7)
2025-12-06 16:48:04,536 - [INFO] - Thread-1 - Producing: DataItem(payload=8)
2025-12-06 16:48:04,584 - [INFO] - Thread-2 - Consuming: 5
2025-12-06 16:48:04,635 - [INFO] - Thread-1 - Producing: DataItem(payload=9)
2025-12-06 16:48:04,685 - [INFO] - Thread-2 - Consuming: 6
2025-12-06 16:48:04,736 - [INFO] - Thread-1 - Producing: DataItem(payload=10)
2025-12-06 16:48:04,786 - [INFO] - Thread-2 - Consuming: 7
2025-12-06 16:48:04,836 - [INFO] - Thread-1 - Producer finished. Sending Poison Pill.
2025-12-06 16:48:04,886 - [INFO] - Thread-2 - Consuming: 8
2025-12-06 16:48:04,986 - [INFO] - Thread-2 - Consuming: 9
2025-12-06 16:48:05,087 - [INFO] - Thread-2 - Consuming: 10
2025-12-06 16:48:05,188 - [INFO] - Thread-2 - Poison Pill received. Shutting down Consumer.
2025-12-06 16:48:05,188 - [INFO] - MainThread - All tasks completed successfully.
```

## Testing

### Run All Tests
```bash
python -m unittest discover -v tests
```

### Run Specific Test Suite
```bash
# Test BlockingQueue
python -m unittest tests.test_blocking_queue

# Test Producer
python -m unittest tests.test_producer

# Test Consumer
python -m unittest tests.test_consumer

# Test DataItem
python -m unittest tests.test_data_item

# Integration Tests
python -m unittest tests.test_integration
```
## Design Details

### BlockingQueue

The `BlockingQueue` class implements a thread-safe bounded buffer:

- **Capacity Control**: Fixed maximum size specified at initialization
- **Thread Synchronization**: Uses `threading.Condition` for wait/notify mechanism
- **Blocking Operations**:
  - `put(item)`: Blocks if queue is full until space becomes available
  - `take()`: Blocks if queue is empty until items are available

**Key Methods:**
```python
put(item: DataItem) -> None    # Add item to queue (blocks if full)
take() -> DataItem             # Remove item from queue (blocks if empty)
```

### Producer Thread

Generates sequential data items and places them into the queue:

- Produces a configurable number of items
- Configurable delay between productions
- Sends a "Poison Pill" (None payload) to signal completion

### Consumer Thread

Retrieves and processes items from the queue:

- Continuously consumes items until receiving a Poison Pill
- Configurable processing time simulation
- Gracefully shuts down upon receiving shutdown signal

### DataItem

Wrapper class for transferred data:

- **Payload**: Any data type
- **Poison Pill Detection**: `is_poison_pill()` method returns `True` when payload is `None`


## Configuration

Modify parameters in `main.py`:
```python
QUEUE_CAPACITY = 3      # Maximum queue size
TOTAL_ITEMS = 10        # Number of items to produce
PRODUCER_DELAY = 0.05   # Delay between productions (seconds)
CONSUMER_DELAY = 0.1    # Simulated processing time (seconds)
```

### Logging Configuration

Adjust logging level in `main.py`:
```python
logging.basicConfig(
    level=logging.INFO,     # Options: DEBUG, INFO, WARNING, ERROR
    format='%(asctime)s - [%(levelname)s] - %(threadName)s - %(message)s'
)
```

##  Key Concepts Demonstrated

#### Thread Synchronization

#### Concurrent Programming


#### Blocking Queue Pattern


#### Wait/Notify Mechanism

