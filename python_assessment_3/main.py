import csv
import json
import event_utils
from event_utils import calculate_booking_amount
import event_utils as eu
# SECTION A: PYTHON BASICS (Q1-Q10)
# Q1-Q4: Booking amount and discount
attendee_name = input("Enter attendee name: ")
tickets = int(input("Enter number of tickets: "))
ticket_price = float(input("Enter ticket price: "))
total_amount = tickets * ticket_price
if total_amount >= 10000:
    discount = total_amount * 0.10
else:
    discount = total_amount * 0.05
final_amount = total_amount - discount
print(f"Attendee Name: {attendee_name}")
print(f"Number of Tickets: {tickets}")
print(f"Ticket Price: Rs. {ticket_price:.2f}")
print(f"Total Booking Amount: Rs. {total_amount:.2f}")
print(f"Discount: Rs. {discount:.2f}")
print(f"Final Amount: Rs. {final_amount:.2f}")
# Q5-Q6: Event capacity
capacity = int(input("\nEnter event capacity: "))
registered = int(input("Enter registered participants: "))
if registered > capacity or registered < 0 or capacity < 0:
    print("Invalid Data")
elif registered == capacity:
    print("Full")
else:
    print("Seats Available")
# Q7: Print numbers 1 to 15
print("\nNumbers from 1 to 15:")
for number in range(1, 16):
    print(number, end=" ")
print()
# Q8: Numbers divisible by 3
print("Numbers divisible by 3:")
for number in range(1, 16):
    if number % 3 == 0:
        print(number, end=" ")
print()
# Q9: Countdown from 10 to 1
print("Countdown:")
count = 10
while count >= 1:
    print(count, end=" ")
    count -= 1
print()
# Q10: break and continue examples
print("Break example:")
for number in range(1, 11):
    if number == 6:
        break
    print(number, end=" ")
print()
print("Continue example (skip 5):")
for number in range(1, 11):
    if number == 5:
        continue
    print(number, end=" ")
print()
# SECTION B: LISTS, TUPLES, SETS, DICTIONARIES (Q11-Q25)
# Q11-Q15
booking_amounts = [5000, 3500, 7500, 6000, 4000, 7000, 3000, 10000]
print("Total booking amounts:", sum(booking_amounts))
print("Average booking amount:", sum(booking_amounts) / len(booking_amounts))
print("Highest amount:", max(booking_amounts))
print("Lowest amount:", min(booking_amounts))
print("Amounts greater than 5000:",
      [amount for amount in booking_amounts if amount > 5000])
print("Sorted descending:", sorted(booking_amounts, reverse=True))
# Q16-Q18
cities = ["Hyderabad", "Mumbai", "Pune", "Hyderabad", "Delhi", "Mumbai"]
unique_cities = set(cities)
print("Unique cities:", unique_cities)
# Q17 Add another city
unique_cities.add("Chennai")
print("Set after adding Chennai:", unique_cities)
# Q18
print("Number of unique cities:", len(unique_cities))
# Q19-Q20
event_details = ("E101", "AI Innovation Summit", "Hyderabad", 500)
print("Event tuple:", event_details)
event_id, event_name, venue, event_capacity = event_details
print("Unpacked event details:")
print(event_id, event_name, venue, event_capacity)
# Q21-Q25
registration = {
    "registration_id": "R1001",
    "attendee_name": "Aarav Shah",
    "city": "Hyderabad",
    "tickets": 2,
    "status": "Pending",
    "amount": 5000
}
print("Q21 Registration dictionary:", registration)
# Q22 Change status
registration["status"] = "Confirmed"
print(" Updated status:", registration["status"])
# Q23 Increase ticket count
registration["tickets"] += 1
print("Updated ticket count:", registration["tickets"])
# Q24 Add email
registration["email"] = "aarav@example.com"
print("Dictionary after adding email:", registration)
# Q25 Loop through dictionary
print("Registration dictionary items:")
for key, value in registration.items():
    print(f"{key}: {value}")
# SECTION C: FUNCTIONS, LAMBDA, FILTER, MAP (Q26-Q35)
# Q26
def calculate_booking(ticket_price, tickets):
    return ticket_price * tickets
print("Booking amount:", calculate_booking(2500, 3))
# Q27
def calculate_discount_amount(amount):
    if amount >= 10000:
        return amount * 0.10
    return amount * 0.05
print("Discount amount:", calculate_discount_amount(12000))
# Q28
def is_active(status):
    return status == "Confirmed"
print("Is Confirmed active?", is_active("Confirmed"))
# Q29
def calculate_total_amount(amounts):
    return sum(amounts)
print("Total amount:", calculate_total_amount(booking_amounts))
# Q30
increase_by_10_percent = lambda amount: amount * 1.10
print("Amount after 10% increase:",increase_by_10_percent(5000))
# Q31
amounts_above_6000 = list(filter(lambda amount: amount > 6000,
                                 booking_amounts))
print("Amounts greater than 6000:", amounts_above_6000)
# Q32: Filter Confirmed registrations
sample_registrations = [
    {"attendee_name": "Aarav Shah", "city": "Hyderabad",
     "status": "Confirmed", "amount": 5000},
    {"attendee_name": "Faiz Ahmed", "city": "Pune",
     "status": "Pending", "amount": 7500},
    {"attendee_name": "Simran Kaur", "city": "Mumbai",
     "status": "Confirmed", "amount": 3500}
]
confirmed_registrations = list(
    filter(lambda item: item["status"] == "Confirmed",
           sample_registrations)
)
print("Confirmed registrations:", confirmed_registrations)
# Q33: Map to extract cities
registration_cities = list(map(
    lambda item: item["city"], sample_registrations
))
print("Registration cities:", registration_cities)
# Q34: Map and set unique cities
unique_registration_cities = set(map(
    lambda item: item["city"], sample_registrations
))
print("Unique registration cities:", unique_registration_cities)
# Q35: Sort registrations by amount
sorted_registrations = sorted(
    sample_registrations,
    key=lambda item: item["amount"]
)
print("Registrations sorted by amount:")
for item in sorted_registrations:
    print(item)
# SECTION D: OBJECT-ORIENTED PROGRAMMING (Q36-Q46)
# Q36-Q38: Event class
class Event:
    def __init__(self, event_id, event_name, capacity, ticket_price):
        self.event_id = event_id
        self.event_name = event_name
        self.capacity = capacity
        self.ticket_price = ticket_price
    def display_event(self):
        print(f"Event ID: {self.event_id}")
        print(f"Event Name: {self.event_name}")
        print(f"Capacity: {self.capacity}")
        print(f"Ticket Price: Rs. {self.ticket_price}")
    def calculate_revenue(self, tickets_sold):
        return tickets_sold * self.ticket_price
# Q39: Create two Event objects
event1 = Event("E101", "AI Innovation Summit", 500, 2500)
event2 = Event("E102", "Leadership Forum", 350, 3500)
print("First event:")
event1.display_event()
print("Second event:")
event2.display_event()
print("Revenue for 10 tickets:", event1.calculate_revenue(10))
# Q40-Q42: OnlineEvent inheritance
class OnlineEvent(Event):
    def __init__(self, event_id, event_name, capacity,
                 ticket_price, platform):
        super().__init__(event_id, event_name, capacity, ticket_price)
        self.platform = platform
    def display_event(self):
        super().display_event()
        print(f"Platform: {self.platform}")
# Q43-Q44: PhysicalEvent
class PhysicalEvent(Event):
    def __init__(self, event_id, event_name, capacity,
                 ticket_price, venue):
        super().__init__(event_id, event_name, capacity, ticket_price)
        self.venue = venue
    def display_event(self):
        super().display_event()
        print(f"Venue: {self.venue}")
online_event = OnlineEvent(
    "E201", "Online Python Workshop", 300, 1000, "Zoom"
)
physical_event = PhysicalEvent(
    "E202", "Technology Conference", 400, 2000, "City Convention Centre"
)
print("Online event:")
online_event.display_event()
print("Physical event:")
physical_event.display_event()
# Q45-Q46: Polymorphism
event_objects = [event1, event2, online_event, physical_event]
print("Display all event objects:")
for event in event_objects:
    print("\nEvent details:")
    event.display_event()
# SECTION E: TEXT FILE HANDLING (Q47-Q52)
# Q47: Write three messages
with open("event_log.txt", "w", encoding="utf-8") as file:
    file.write("Event registration processing started.\n")
    file.write("Registration records are being processed.\n")
    file.write("Event processing completed.\n")
# Q48: Append two more messages
with open("event_log.txt", "a", encoding="utf-8") as file:
    file.write("Staff records are being processed.\n")
    file.write("Event analytics completed.\n")
# Q49: Read complete file
with open("event_log.txt", "r", encoding="utf-8") as file:
    print(" Complete event log:")
    print(file.read(), end="")
# Q50-Q51: Read line by line without extra blank lines
print("Event log line by line:")
with open("event_log.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.rstrip("\n"))
# SECTION F: CSV WITHOUT PANDAS (Q53-Q60)
with open("registrations.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    registrations = list(reader)
# Q53-Q54
print("Total records read:", len(registrations))
# Convert numeric fields
for record in registrations:
    record["tickets"] = int(record["tickets"])
    record["amount"] = float(record["amount"])
# Q55
print("\nConfirmed registrations:")
for record in registrations:
    if record["status"] == "Confirmed":
        print(record)
# Q56
print("\nRegistrations from Hyderabad:")
for record in registrations:
    if record["city"] == "Hyderabad":
        print(record)
# Q57
print("\nAmounts converted to numeric:")
for record in registrations:
    print(record["registration_id"], record["amount"],
          type(record["amount"]).__name__)
# Q58
print("\nRegistrations with amount greater than 7000:")
for record in registrations:
    if record["amount"] > 7000:
        print(record)
# Q59
total_registration_amount = sum(
    record["amount"] for record in registrations
)
print("\nTotal registration amount:", total_registration_amount)
# Q60
registration_city_list = [record["city"] for record in registrations]
unique_registration_city_list = set(registration_city_list)
print("All cities:", registration_city_list)
print("Unique cities:", unique_registration_city_list)
# SECTION G: JSON PROCESSING (Q61-Q74)
with open("staff.json", "r", encoding="utf-8") as file:
    staff = json.load(file)
# Q61-Q62
print("JSON data loaded.")
print("Data type:", type(staff).__name__)
# Q63
print("\nStaff names:")
for person in staff:
    print(person["name"])
# Q64
print("\nOperations employees:")
for person in staff:
    if person["department"] == "Operations":
        print(person["name"])
# Q65
print("\nEmployees with salary greater than 75000:")
for person in staff:
    if person["salary"] > 75000:
        print(person["name"], person["salary"])
# Q66
print("\nStaff with Python skill:")
for person in staff:
    if "Python" in person["skills"]:
        print(person["name"])
# Q67
print("\nName, Rating, Events Handled:")
for person in staff:
    print(
        person["name"],
        person["performance"]["rating"],
        person["performance"]["events_handled"]
    )
# Q68
print("\nStaff with rating greater than 4.5:")
for person in staff:
    if person["performance"]["rating"] > 4.5:
        print(person["name"], person["performance"]["rating"])
# Q69
all_skills = []
for person in staff:
    all_skills.extend(person["skills"])
print("\n All skills:", all_skills)
# Q70
unique_skills = set(all_skills)
print("Unique skills:", unique_skills)
# Q71
staff_by_salary = sorted(
    staff, key=lambda person: person["salary"], reverse=True
)
print("\nStaff sorted by salary descending:")
for person in staff_by_salary:
    print(person["name"], person["salary"])
# Q72
staff_by_rating = sorted(
    staff,
    key=lambda person: person["performance"]["rating"],
    reverse=True
)
print("\nStaff sorted by rating descending:")
for person in staff_by_rating:
    print(person["name"], person["performance"]["rating"])
# Q73: Add Pandas skill to staff_id 503
for person in staff:
    if person["staff_id"] == 503:
        if "Pandas" not in person["skills"]:
            person["skills"].append("Pandas")
print("\n Updated skills for staff_id 503:")
for person in staff:
    if person["staff_id"] == 503:
        print(person["name"], person["skills"])
# Q74: Save updated JSON separately
with open("staff_updated.json", "w", encoding="utf-8") as file:
    json.dump(staff, file, indent=2)
print(" Updated staff data saved to staff_updated.json")
# SECTION H: MODULES (Q75-Q79)
# Q75-Q77: Use the imported module
module_amount = event_utils.calculate_booking_amount(2500, 4)
module_discount = event_utils.calculate_discount(module_amount)
module_capacity = event_utils.check_event_capacity(100, 80)
print(" amount:", module_amount)
print("Discount:", module_discount)
print(" Capacity status:", module_capacity)
# Q78: Import and call one function directly
direct_amount = calculate_booking_amount(1500, 3)
print("\nDirectly imported function result:", direct_amount)
# Q79: Import module using alias
alias_discount = eu.calculate_discount(12000)
print("Module alias discount result:", alias_discount)
# SECTION I: PANDAS BASICS (Q80-Q88)
try:
    import pandas as pd
    # Q80
    df = pd.read_csv("registrations.csv")
    print("DataFrame loaded successfully.")
    # Q81
    print("\nFirst five rows:")
    print(df.head())
    print("\nLast five rows:")
    print(df.tail())
    print("\nShape:")
    print(df.shape)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nData types:")
    print(df.dtypes)
    # Q82
    print("\nSelected columns:")
    print(df[["attendee_name", "city", "status", "amount"]])
    # Q83
    print("\nConfirmed registrations:")
    print(df.query("status == 'Confirmed'"))
    # Q84
    print("\nRegistrations with amount greater than 6000:")
    print(df.query("amount > 6000"))
    # Q85
    print("\nConfirmed registrations from Hyderabad:")
    print(df.query("status == 'Confirmed' and city == 'Hyderabad'"))
    # Q86
    print("\nRegistration count by status:")
    print(df.groupby("status").size())
    # Q87
    print("\nTotal amount by status:")
    print(df.groupby("status")["amount"].sum())
    # Q88
    print("\nAverage amount by city:")
    print(df.groupby("city")["amount"].mean())
except ImportError:
    print("Pandas is not installed.")
    print("Install it using: python -m pip install pandas")
    print("Then run main.py again.")
print("\n========== ALL ASSESSMENT SECTIONS COMPLETED ==========")