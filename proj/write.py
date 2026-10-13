import csv
with open('products.csv', "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "product_id",
        "product_name",
        "category"
        "price"
    ])
    writer.writerow(['101',"Laptop", "Electronics", 65000])
    writer.writerow(['102',"Mouse", "Accessories", 15000])
    writer.writerow([103, "Office Chair", "Furniture", 9000])
    writer.writerow([104, "Monitor", "Electronics", 18000])
