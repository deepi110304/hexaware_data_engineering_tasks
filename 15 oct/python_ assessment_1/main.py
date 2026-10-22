import csv
import json
import pandas as pd
import numpy as np
import retail_utils
import retail_utils as ru
from retail_utils import calculate_order_total
# SECTION A: PYTHON BASICS (1-9)
product_name = input("Enter product name: ")
unit_price = float(input("Enter unit price: "))
quantity = int(input("Enter quantity: "))
total_amount = unit_price * quantity
discount = retail_utils.calculate_discount(total_amount)
final_amount = total_amount - discount
print(f"Original Amount: {total_amount:.2f}")
print(f"Discount: {discount:.2f}")
print(f"Final Amount: {final_amount:.2f}")
stock = int(input("Enter stock quantity: "))
print(retail_utils.check_stock(stock))
for i in range(1, 11):
    print(i)
stock = 5
while stock >= 0:
    print(stock)
    stock -= 1
for i in range(1, 11):
    if i == 5:
        continue
    print(i)

for i in range(1, 11):
    if i == 8:
        break
    print(i)
# SECTION B: COLLECTIONS (10-20)
sales = [65000, 4500, 36000, 12000, 18000, 72000, 9000]
print("Total Sales:", sum(sales))
print("Highest Sale:", max(sales))
print("Lowest Sale:", min(sales))
print("Sales above 20000:", [s for s in sales if s > 20000])
print("Descending Sales:", sorted(sales, reverse=True))
cities = [
    "Hyderabad", "Mumbai", "Delhi",
    "Hyderabad", "Pune", "Mumbai"
]
print("Unique Cities:", set(cities))
product = (201, "Laptop", "Electronics", 65000)
product_id, product_name, category, price = product
print(product_id, product_name, category, price)
customer = {
    "ID": "C101",
    "Name": "North Star Retail",
    "City": "Hyderabad",
    "Orders": 3,
    "Active": True
}
customer["City"] = "Mumbai"
customer["Orders"] += 1
customer["Email"] = "customer@example.com"
for key, value in customer.items():
    print(key, ":", value)
# SECTION C: FUNCTIONS AND LAMBDA (21-29)
def calculate_total(price, quantity):
    return price * quantity
def calculate_discount(amount):
    if amount >= 50000:
        return amount * 0.10
    return amount * 0.05
def total_sales(sales):
    return sum(sales)
def check_product_stock(product):
    if product["stock"] > 0:
        return "Available"
    return "Out of Stock"
square = lambda n: n * n
print("Square:", square(5))
print(
    "Filtered Sales:",
    list(filter(lambda x: x > 20000, sales))
)
customers_sample = [
    {"name": "North Star Retail", "city": "Hyderabad"},
    {"name": "Blue Mart", "city": "Mumbai"},
    {"name": "Daily Basket", "city": "Bangalore"}
]
customer_cities = list(
    map(lambda c: c["city"], customers_sample)
)
print(customer_cities)
print(set(customer_cities))
products_sample = [
    {"product_name": "Laptop", "price": 65000},
    {"product_name": "Monitor", "price": 18000},
    {"product_name": "Office Chair", "price": 9000},
    {"product_name": "Keyboard", "price": 3000}
]
print(sorted(products_sample, key=lambda p: p["price"]))
# SECTION D: OOP (30-39)
class Product:
    def __init__(self, product_id, product_name, price, stock):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.stock = stock
    def display_product(self):
        print(
            self.product_id,
            self.product_name,
            self.price,
            self.stock
        )
    def calculate_value(self):
        return self.price * self.stock
class DiscountedProduct(Product):
    def __init__(
        self, product_id, product_name, price, stock,
        discount_percent
    ):
        super().__init__(product_id, product_name, price, stock)
        self.discount_percent = discount_percent
    def display_product(self):
        super().display_product()
        print("Discount:", self.discount_percent, "%")
class PremiumProduct(Product):
    def display_product(self):
        print("Premium Product:")
        super().display_product()
p1 = Product(201, "Laptop", 65000, 12)
p2 = Product(202, "Monitor", 18000, 8)
p3 = DiscountedProduct(203, "Office Chair", 9000, 15, 10)
p4 = PremiumProduct(204, "Keyboard", 3000, 30)
print("Stock Value:", p1.calculate_value())
for p in [p1, p3, p4]:
    p.display_product()
# SECTION E: TEXT, CSV AND JSON FILES (40-55)
# Q40-Q43: Create, write, append and read activity.txt
with open("activity.txt", "w") as file:
    file.write("Order processing started.\n")
    file.write("Customer records processed.\n")
    file.write("Product records processed.\n")
with open("activity.txt", "a") as file:
    file.write("Order processing completed.\n")
with open("activity.txt", "r") as file:
    print(file.read())
# Read customers.csv
with open("customers.csv", "r", newline="") as file:
    customer_records = list(csv.DictReader(file))
print("All Customers:", customer_records)
print("Active Customers:")
for c in customer_records:
    if c["active"] == "True":
        print(c)
print("Hyderabad Customers:")
for c in customer_records:
    if c["city"] == "Hyderabad":
        print(c)
# Read products.json
with open("products.json", "r") as file:
    product_records = json.load(file)
print("Product Names:")
for p in product_records:
    print(p["product_name"])
print("Products above 10000:")
for p in product_records:
    if p["price"] > 10000:
        print(p["product_name"], p["price"])
print("Supplier Details:")
for p in product_records:
    print(p["supplier"]["name"], p["supplier"]["city"])
all_colors = []
for p in product_records:
    all_colors.extend(p["colors"])
print("All Colors:", all_colors)
print("Unique Colors:", set(all_colors))
# Increase stock of product ID 202
for p in product_records:
    if p["product_id"] == 202:
        p["stock"] += 1
with open("products_updated.json", "w") as file:
    json.dump(product_records, file, indent=4)
# SECTION F: USER-DEFINED MODULE (56-60)
print(retail_utils.calculate_order_total(65000, 1))
print(retail_utils.calculate_discount(65000))
print(retail_utils.check_stock(12))
print(calculate_order_total(3000, 4))
print(ru.calculate_discount(72000))
# SECTION G: PANDAS DATA PROCESSING (61-74)
# Q61: Read CSV into a Pandas DataFrame
orders = pd.read_csv("orders.csv")
# The provided CSV header is "stat"; rename it to "status"
orders.rename(columns={"stat": "status"}, inplace=True)
# Q62: Display first 5 rows
print("\nFirst 5 Rows:")
print(orders.head())
# Q63: Display column names and data types
print("\nColumn Names and Data Types:")
print(orders.dtypes)
# Q64: Display shape of DataFrame
print("\nDataFrame Shape:")
print(orders.shape)
# Q65: Filter Delivered orders using query()
print("\nDelivered Orders:")
print(orders.query("status == 'Delivered'"))
# Q66: Filter orders where quantity is greater than 2
print("\nQuantity Greater Than 2:")
print(orders[orders["quantity"] > 2])
# Q67: Calculate order value
orders["order_value"] = orders["quantity"] * orders["unit_price"]
print("\nOrder Value:")
print(orders[["order_id", "order_value"]])
# Q68: Count orders by status
print("\nOrders By Status:")
print(orders["status"].value_counts())
# Q69: Convert order_date to datetime
orders["order_date"] = pd.to_datetime(orders["order_date"])
# Q70: Create month column
orders["month"] = orders["order_date"].dt.month
# Q71: Order count by month and status
print("\nOrder Count By Month and Status:")
print(orders.groupby(["month", "status"]).size())
# Q72: Total order value by category
print("\nTotal Order Value By Category:")
print(orders.groupby("category")["order_value"].sum())
# Q73: Average order value by category
print("\nAverage Order Value By Category:")
print(orders.groupby("category")["order_value"].mean())
# Q74: Sort orders by order value descending
orders = orders.sort_values("order_value", ascending=False)
print("\nOrders Sorted By Order Value:")
print(orders)
# SECTION H: PANDAS JOIN AND AGGREGATION (75-81)
customers = pd.read_csv("customers.csv")
# Q75: Perform inner join using customer_id
joined = pd.merge(
    orders,
    customers,
    on="customer_id",
    how="inner"
)
# Q76: Display selected joined order details
print("\nJoined Order Details:")
print(
    joined[
        [
            "order_id",
            "customer_name",
            "city",
            "product",
            "status",
            "order_value"
        ]
    ]
)
# Q77: Delivered orders from Hyderabad
print("\nDelivered Orders From Hyderabad:")
print(
    joined[
        (joined["status"] == "Delivered") &
        (joined["city"] == "Hyderabad")
    ]
)
# Q78: Calculate city-wise order and sales summary
city_summary = joined.groupby("city").agg(
    total_orders=("order_id", "count"),
    total_sales=("order_value", "sum"),
    average_order_value=("order_value", "mean")
).reset_index()
# Q79: Sort city results by total sales descending
city_summary = city_summary.sort_values(
    "total_sales",
    ascending=False
)
print("\nCity Sales Summary:")
print(city_summary)
# Q80: Save city summary as CSV
city_summary.to_csv("city_sales_summary.csv", index=False)
# Q81: Save city summary as JSON
city_summary.to_json(
    "city_sales_summary.json",
    orient="records",
    indent=4
)
# SECTION I: NUMPY/PANDAS ENRICHMENT (82-84)
# Q82: Create order_size using NumPy
joined["order_size"] = np.select(
    [
        joined["order_value"] >= 50000,
        joined["order_value"] >= 15000
    ],
    [
        "High",
        "Medium"
    ],
    default="Low"
)
# Q83: Mark Corporate customers as Priority, others Normal
joined["priority_customer"] = np.where(
    joined["segment"] == "Corporate",
    "Priority",
    "Normal"
)
print("\nEnriched Orders:")
print(joined)
# Q84: Save enriched dataset
joined.to_csv("enriched_orders.csv", index=False)
print("\nSections G-I completed successfully.")
print("Created: products_updated.json")
print("Created: city_sales_summary.csv")
print("Created: city_sales_summary.json")
print("Created: enriched_orders.csv")