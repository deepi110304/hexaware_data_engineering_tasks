import update
products = [
    {
        "product_id": 101,
        "product_name": "Laptop",
        "category": "Electronics",
        "price": 65000
    },
    {
        "product_id": 102,
        "product_name": "Mouse",
        "category": "Accessories",
        "price": 1500
    },
    {
        "product_id": 103,
        "product_name": "Monitor",
        "category": "Electronics",
        "price": 18000
    }
]

with open("products.json", "w") as file:
    update.dump(products, file, indent=4)