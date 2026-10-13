product = {
    "product_id": 101,
    "product_name": "Laptop",
    "category": "Electronics",
    "price": 65000
}
print(product)
print(product["product_name"])
#get without error
print(product.get("brand"))
product["price"] = 70000
product["stock"] = 20
print(product)
#remove
product.pop("category")
del product["price"]