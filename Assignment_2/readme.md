# Assignment 2 - Functional Car Sales Analysis

## Project Description
A Python application that analyzes car sales data using **Functional Programming** paradigms and **Stream processing**. The application reads a CSV dataset of car sales and performs aggregation to identify:
1. The most selling car model (by quantity).
2. The most profitable car model (by total revenue).
3. Global statistics (Total Revenue, Unique Models).

## Technologies
* **Language:** Python 3.x
* **Paradigms:** Functional Programming (Map/Reduce/Filter), Lazy Evaluation (Generators/Streams).
* **Testing:** `unittest` framework with `unittest.mock`.

## Assumptions & Design Choices

### 1. Stream Operations (Lazy Evaluation)
* **Choice:** I used Python Generators (`yield`) in `src/streams.py` instead of loading the CSV into a Pandas DataFrame or a list.
* **Reasoning:** This satisfies the "Stream operations" requirement. It ensures the application remains memory-efficient (O(1) memory) even if the input CSV grows to gigabytes in size.

### 2. Functional Programming
* **Choice:** I implemented a generic `functional_aggregate` function in `src/analysis.py` that uses `functools.reduce`.
* **Choice:** Immutability is enforced using a `@dataclass(frozen=True)` for the `CarSale` model.
* **Reasoning:** This prevents side effects during data processing. Logic is injected via **Lambda expressions** in `main.py`, keeping the core analysis functions pure and reusable.

### 3. Data Integrity & Assumptions
* **Assumption:** A "Car Model" is defined as the unique combination of `brand` + `model`.
* **Assumption:** "Revenue" is calculated as the sum of the `price` column for all matching records.
* **Error Handling:** The stream reader gracefully skips rows with malformed data (e.g., non-numeric prices) and catches missing file errors without crashing the application.

## How to Run

1.  **Place Data:** Ensure `Car_sales_dataset.csv` is inside the `data/` folder.
2.  **Run Application:**
    ```bash
    python main.py
    ```
### Sample Output 
    ```
        Total Revenue:  $46,900,411.00
        • Unique Models:  180
        --------------------------------------------------
        1. Most Selling Car (Quantity):
        • Model: ford door
        • Units: 363.0
        • Rev:   $5,242,254.00

        2. Most Profitable Car (Revenue):
        • Model: ford f-150
        • Units: 219.0
        • Rev:   $6,175,108.00
        • Share: 13.17% of total market revenue
    ```
3.  **Run Tests:**
    ```bash
    python -m unittest discover -v tests

    ```
