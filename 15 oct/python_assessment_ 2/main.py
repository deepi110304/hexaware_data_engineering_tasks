import csv
import json
import pandas as pd
import numpy as np
import shipment_utils
from shipment_utils import calculate_cost_per_kg
# SECTION A: PYTHON FUNDAMENTALS (Q1-Q6)
weight = float(input("Enter shipment weight in kg: "))
cost = float(input("Enter shipment cost: "))
cost_per_kg = calculate_cost_per_kg(cost, weight)
print("Cost per kg:", round(cost_per_kg, 2))
print("Weight category:", shipment_utils.classify_weight(weight))
print("\nShipment numbers from 1 to 20:")
for number in range(1, 21):
    print(number, end=" ")
print("\n\nEven shipment numbers:")
for number in range(1, 21):
    if number % 2 == 0:
        print(number, end=" ")
print("\n\nProcessing attempts:")
attempt = 1
while attempt <= 5:
    print("Processing attempt", attempt)
    attempt += 1
# SECTION B: COLLECTIONS (Q7-Q12)
print("\n\n===== SECTION B: COLLECTIONS =====")
shipment_costs = [
    850, 620, 1250, 480, 1600, 740,
    590, 1100, 920, 1750, 520, 1050
]
print("Shipment costs:", shipment_costs)
print("Total cost:", sum(shipment_costs))
print("Average cost:", sum(shipment_costs) / len(shipment_costs))
print("Minimum cost:", min(shipment_costs))
print("Maximum cost:", max(shipment_costs))
destinations = [
    "Hyderabad", "Mumbai", "Bangalore", "Delhi",
    "Pune", "Hyderabad", "Mumbai", "Delhi",
    "Bangalore", "Pune", "Hyderabad", "Mumbai"
]
unique_destinations = set(destinations)
print("Unique destinations:", unique_destinations)
one_shipment = {
    "shipment_id": "S1001",
    "destination": "Hyderabad",
    "weight": 12.5,
    "status": "Delivered",
    "cost": 850
}
print("One shipment:", one_shipment)
shipments = [
    {"shipment_id": "S1001", "destination": "Hyderabad",
     "weight": 12.5, "status": "Delivered", "cost": 850},
    {"shipment_id": "S1002", "destination": "Mumbai",
     "weight": 8.0, "status": "In Transit", "cost": 620},
    {"shipment_id": "S1003", "destination": "Bangalore",
     "weight": 18.5, "status": "Delivered", "cost": 1250},
    {"shipment_id": "S1004", "destination": "Delhi",
     "weight": 5.5, "status": "Pending", "cost": 480},
    {"shipment_id": "S1005", "destination": "Pune",
     "weight": 22.0, "status": "Delivered", "cost": 1600},
    {"shipment_id": "S1006", "destination": "Hyderabad",
     "weight": 10.0, "status": "In Transit", "cost": 740},
    {"shipment_id": "S1007", "destination": "Mumbai",
     "weight": 7.2, "status": "Delivered", "cost": 590},
    {"shipment_id": "S1008", "destination": "Delhi",
     "weight": 15.5, "status": "Pending", "cost": 1100},
    {"shipment_id": "S1009", "destination": "Bangalore",
     "weight": 11.8, "status": "Delivered", "cost": 920},
    {"shipment_id": "S1010", "destination": "Pune",
     "weight": 25.0, "status": "Delivered", "cost": 1750},
    {"shipment_id": "S1011", "destination": "Hyderabad",
     "weight": 6.5, "status": "In Transit", "cost": 520},
    {"shipment_id": "S1012", "destination": "Mumbai",
     "weight": 14.0, "status": "Delivered", "cost": 1050}
]
delivered_shipments = [
    shipment for shipment in shipments
    if shipment["status"] == "Delivered"
]
print("Delivered shipments:", delivered_shipments)
# SECTION C: FUNCTIONS AND LAMBDA (Q13-Q17)
def shipping_cost(weight):
    return shipment_utils.calculate_shipping_cost(weight)
def shipment_category(weight):
    return shipment_utils.get_shipment_category(weight)
print("Shipping cost for 10 kg:", shipping_cost(10))
print("Category for 15 kg:", shipment_category(15))
delivered = list(filter(
    lambda shipment: shipment["status"] == "Delivered",
    shipments
))
print("Delivered shipments using filter:", delivered)
all_destinations = list(map(
    lambda shipment: shipment["destination"],
    shipments
))
print("All destinations using map:", all_destinations)
sorted_shipments = sorted(
    shipments,
    key=lambda shipment: shipment["cost"]
)
print("Shipments sorted by cost:")
for shipment in sorted_shipments:
    print(shipment)
# SECTION D: OOP (Q18-Q23)
class Shipment:
    def __init__(self, shipment_id, destination, weight, cost):
        self.shipment_id = shipment_id
        self.destination = destination
        self.weight = weight
        self.cost = cost
    def display(self):
        print(
            "Shipment ID:", self.shipment_id,
            "| Destination:", self.destination,
            "| Weight:", self.weight,
            "| Cost:", self.cost
        )
class ExpressShipment(Shipment):
    def display(self):
        express_cost = shipment_utils.add_express_surcharge(self.cost)
        print(
            "Express Shipment ID:", self.shipment_id,
            "| Destination:", self.destination,
            "| Weight:", self.weight,
            "| Original Cost:", self.cost,
            "| Cost with Express Surcharge:", express_cost
        )
normal_shipment = Shipment("S1001", "Hyderabad", 12.5, 850)
express_shipment = ExpressShipment("S1002", "Mumbai", 8.0, 620)
print("Normal shipment:")
normal_shipment.display()
print("Express shipment:")
express_shipment.display()
print("Polymorphism:")
for item in [normal_shipment, express_shipment]:
    item.display()
# SECTION E: JSON PROCESSING (Q24-Q32)
with open("employees.json", "r") as file:
    employees = json.load(file)
print("All employee names:")
for employee in employees:
    print(employee["name"])
print("\nEmployees earning above 75000:")
for employee in employees:
    if employee["salary"] > 75000:
        print(employee["name"], employee["salary"])
print("\nEmployees knowing Python:")
for employee in employees:
    if "Python" in employee["skills"]:
        print(employee["name"])
print("\nEmployee performance ratings:")
for employee in employees:
    print(
        employee["name"],
        employee["performance"]["rating"]
    )
print("\nEmployees with rating above 4.5:")
for employee in employees:
    if employee["performance"]["rating"] > 4.5:
        print(employee["name"])
sorted_employees = sorted(
    employees,
    key=lambda employee: employee["performance"]["rating"],
    reverse=True
)
print("\nEmployees sorted by rating descending:")
for employee in sorted_employees:
    print(employee["name"],employee["performance"]["rating"])
for employee in employees:
    if employee["employee_id"] == 303:
        if "Python" not in employee["skills"]:
            employee["skills"].append("Python")
        break
with open("employees_updated.json", "w") as file:
    json.dump(employees, file, indent=4)
print("Updated employee data saved to employees_updated.json")
# SECTION F: MODULES (Q33-Q35)
sample_weight = 12.5
sample_cost = 850
print("Cost per kg using module:",shipment_utils.calculate_cost_per_kg(sample_cost, sample_weight))
print("Weight category using module:", shipment_utils.classify_weight(sample_weight))
print("Cost per kg using specific import:",calculate_cost_per_kg(sample_cost, sample_weight))
# SECTION G: PANDAS (Q36-Q43)
print("\n===== SECTION G: PANDAS =====")
df = pd.read_csv("shipments.csv")
print("\nAll shipments:")
print(df)
print("\nDelivered shipments:")
delivered_df = df[df["status"] == "Delivered"]
print(delivered_df)
print("\nCount of records by status:")
print(df["status"].value_counts())
df["shipment_date"] = pd.to_datetime(df["shipment_date"])
df["month"] = df["shipment_date"].dt.month
print("\nShipment count by month and status:")
print(pd.crosstab(df["month"], df["status"]))
print("\nAverage cost by destination:")
print(df.groupby("destination")["cost"].mean())
print("\nTotal weight by destination:")
print(df.groupby("destination")["weight"].sum())
selected_columns = ["shipment_id", "destination", "status", "cost"]
selected_df = pd.read_csv("shipments.csv", usecols=selected_columns)
print("\nSelected columns using usecols:")
print(selected_df)
# SECTION H: JOIN AND AGGREGATION (Q44-Q50)
hubs_df = pd.read_csv("hubs.csv")
merged_df = pd.merge(
    df,
    hubs_df,
    on="hub_id",
    how="inner"
)
print("\nShipments joined with hubs:")
print(merged_df)
hub_cost = merged_df.groupby(
    ["hub_id", "hub_name"]
)["cost"].sum().reset_index(name="total_shipment_cost")
print("\nTotal shipment cost handled by each hub:")
print(hub_cost)
hub_count = merged_df.groupby(
    ["hub_id", "hub_name"]
).size().reset_index(name="total_shipments")
print("\nTotal shipments handled by each hub:")
print(hub_count)
hub_summary = pd.merge(
    hub_cost,
    hub_count,
    on=["hub_id", "hub_name"]
)
hub_summary = hub_summary.sort_values(
    by="total_shipment_cost",
    ascending=False
)
print("\nHub summary sorted by total cost:")
print(hub_summary)
hub_summary.to_csv("hub_summary.csv", index=False)
hub_summary.to_json("hub_summary.json", orient="records", indent=4)
print("Saved hub_summary.csv and hub_summary.json")
# SECTION I: NUMPY AND DATA ENRICHMENT (Q51-Q54)
df["cost_per_kg"] = df["cost"] / df["weight"]
df["cost_category"] = np.where(
    df["cost"] >= 1200,
    "Expensive",
    "Normal"
)
conditions = [
    (df["status"] == "Delivered") & (df["cost"] >= 1200),
    (df["status"] == "Delivered") & (df["cost"] < 1200),
    (df["status"] == "In Transit") & (df["cost"] >= 1200),
    (df["status"] == "In Transit") & (df["cost"] < 1200),
    (df["status"] == "Pending") & (df["cost"] >= 1200),
    (df["status"] == "Pending") & (df["cost"] < 1200)
]
categories = [
    "High Value Delivered",
    "Standard Delivered",
    "High Cost In Transit",
    "Standard In Transit",
    "High Cost Pending",
    "Standard Pending"
]
df["shipment_performance"] = np.select(
    conditions,
    categories,
    default="Other"
)
df.to_csv("shipment_analysis.csv", index=False)
print("\nFinal enriched shipment dataset:")
print(df)
print("\nSaved final dataset as shipment_analysis.csv")
print("\nAll Assessment 2 sections completed.")