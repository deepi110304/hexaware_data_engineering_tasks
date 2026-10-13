cities = {"Hyderabad", "Mumbai", "Delhi", "Bangalore"} # set
print(cities)

cities.add("Pune")
print(cities)

cities.remove("Mumbai")
print(cities)

# Safer option to remove 
cities.discard("Chennai")
print(cities)

cities_list = [
    "Hyderabad",
    "Mumbai",
    "Delhi",
    "Hyderabad",
    "Mumbai",
]
unique_cities = set(cities_list)
print(unique_cities)