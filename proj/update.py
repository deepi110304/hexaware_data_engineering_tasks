import json

with open("products.json", "r") as file:
    products = json.load(file)

print(products)

# Modify the json
import json
with open("products.json", "r") as file:
    products = json.load(file)
for product in products:
    if product["product_id"] == 101:
        product["price"] = 70000

with open("products.json", "w") as file:
    json.dump(products, file, indent=4)
