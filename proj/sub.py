import csv
with open('products.csv', "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
#########################################
import csv
with open('products.csv', "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)