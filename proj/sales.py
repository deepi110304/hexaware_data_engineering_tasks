sales = [
    ("North", 12000),
    ("South", 18000),
    ("West", 9500),
    ("North", 22000),
    ("East", 15000),
    ("South", 11000)
]
# TASK 1
print("1. All tuples:")
for s in sales:
    print(s)
# TASK 2
print("\n2. Only Regions:")
for region, amount in sales:
    print(region)
print(list(map(lambda x: x[0], sales)))
# TASK 3
print("\n3. Only Sales Amount:")
for region, amount in sales:
    print(amount)
print(list(map(lambda x: x[1], sales)))
# TASK 4
print("\n4. Sales > 12000:")
greater = list(filter(lambda x: x[1] > 12000, sales))
for s in greater:
    print(s)
# TASK 5
print("\n5. Total Sales:")
total = sum(amount for region, amount in sales)
print(total)
# TASK 6
print("\n6. Highest and Lowest:")
amounts = [amount for region, amount in sales]
print("Highest:", max(amounts))
print("Lowest:", min(amounts))
# TASK 7
print("\n7. List of only sales amounts:")
only_amounts = list(map(lambda x: x[1], sales))
print(only_amounts)
# TASK 8
print("\n8. Unique Regions:")
unique_regions = set(map(lambda x: x[0], sales))
print(unique_regions)
# TASK 9
print("\n9. Sorted by Sales Amount (low to high):")
by_amount = sorted(sales, key=lambda x: x[1])
for s in by_amount:
    print(s)
# TASK 10
print("\n10. Sorted by Region Name:")
by_region = sorted(sales, key=lambda x: x[0])
for s in by_region:
    print(s)