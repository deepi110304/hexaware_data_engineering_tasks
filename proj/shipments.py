import csv, os
print("Current folder:", os.getcwd())
shipments = []
try:
    with open("shipments.csv", "r") as file:
        reader = csv.DictReader(file)
        print("CSV Headers:", reader.fieldnames)
        for row in reader:
            shipments.append(row)
except FileNotFoundError:
    print("ERROR: shipments.csv file not found!")
    exit()
print(f"Total records read: {len(shipments)}")
# TASK 3
print("\n3. Complete List:")
for s in shipments:
    print(s)
# TASK 4
print("\n4. ID, Customer, Status:")
for s in shipments:
    print(s['shipment_id'], s['customer'], s['status'])
# TASK 5
for s in shipments:
    s['weight'] = float(s['weight'])
    s['cost'] = int(s['cost'])
# TASK 6
total_cost = sum(s['cost'] for s in shipments)
print(f"\n6. Total Shipping Cost: {total_cost}")
# TASK 7
print("\n7. Cost > 700:")
for s in [x for x in shipments if x['cost'] > 700]:
    print(s)
# TASK 8
print("\n8. Delivered Shipments (filter + lambda):")
delivered = list(filter(lambda x: x['status'] == 'Delivered', shipments))
for s in delivered:
    print(s)
# TASK 9
print("\n9. Weight > 10 (filter + lambda):")
heavy = list(filter(lambda x: x['weight'] > 10, shipments))
for s in heavy:
    print(s)
# TASK 10
print("\n10. All City Names (map):")
print(list(map(lambda x: x['city'], shipments)))
# TASK 11
print("\n11. Unique Cities (map + set):")
print(set(map(lambda x: x['city'], shipments)))
# TASK 12
print("\n12. Sorted by Cost (Low to High):")
for s in sorted(shipments, key=lambda x: x['cost']):
    print(s['shipment_id'], s['cost'])
# TASK 13
print("\n13. Sorted by Weight High to Low:")
for s in sorted(shipments, key=lambda x: x['weight'], reverse=True):
    print(s['shipment_id'], s['weight'])
# TASK 14
print("\n14. Sorted by Customer Name:")
for s in sorted(shipments, key=lambda x: x['customer']):
    print(s['customer'])
# TASK 15
print("\n15. Cost per KG:")
cost_per_kg = lambda cost, weight: cost / weight
for s in shipments:
    print(f"{s['shipment_id']}: {cost_per_kg(s['cost'], s['weight']):.2f} per kg")