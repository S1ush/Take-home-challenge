import os
from src.streams import car_sales_stream
from src.analysis import functional_aggregate, get_max_entry

DATA_PATH = os.path.join("data", "Car_sales_dataset.csv")

def main():
    print("--- Functional Car Sales Analysis ---\n")
    
    # Initialize Stream
    # We create the stream generator. No data is read yet (Lazy Evaluation).
    stream = car_sales_stream(DATA_PATH)
    
    # Execute Aggregation
    sales_map = functional_aggregate(
        stream,
        key_selector=lambda c: c.full_name,              # Group by "Brand Model"
        value_mapper=lambda c: {'count': 1, 'revenue': c.price}  # Extract 1 unit and price
    )
    
    # Calculate Global Stats
    total_revenue = sum(map(lambda x: x['revenue'], sales_map.values()))
    total_models = len(sales_map)
    
    print(f"Global Stats:")
    print(f"• Total Revenue:  ${total_revenue:,.2f}")
    print(f"• Unique Models:  {total_models}")
    print("-" * 50)

    # Most Selling Car (by Quantity)
    # We pass a lambda to define "Most Selling" as "highest count"
    best_seller, seller_stats = get_max_entry(
        sales_map, 
        comparator=lambda x: x['count']
    )
    
    print(f"1. Most Selling Car (Quantity):")
    print(f"   • Model: {best_seller}")
    print(f"   • Units: {seller_stats['count']}")
    print(f"   • Rev:   ${seller_stats['revenue']:,.2f}")
    
    # Most Profitable Car (by Revenue)
    most_profit, profit_stats = get_max_entry(
        sales_map, 
        comparator=lambda x: x['revenue']
    )
    
    percentage = (profit_stats['revenue'] / total_revenue * 100) if total_revenue else 0
    
    print(f"\n2. Most Profitable Car (Revenue):")
    print(f"   • Model: {most_profit}")
    print(f"   • Units: {profit_stats['count']}")
    print(f"   • Rev:   ${profit_stats['revenue']:,.2f}")
    print(f"   • Share: {percentage:.2f}% of total market revenue")

if __name__ == "__main__":
    main()