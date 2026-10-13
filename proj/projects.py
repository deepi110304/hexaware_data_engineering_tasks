import json
# TASK 1
with open("projects.json", "r") as file:
    projects = json.load(file)
# TASK 2
print("2. Datatype:", type(projects))
# TASK 3
print("\n3. All Project Names:")
for p in projects:
    print(p["project_name"])
# TASK 4
print("\n4. Budget > 400000:")
for p in projects:
    if p["budget"] > 400000:
        print(p["project_name"], "-", p["budget"])
high_budget = list(filter(lambda x: x["budget"] > 400000, projects))
print("Using filter:", [p["project_name"] for p in high_budget])
# TASK 5
print("\n5. Projects that use Python:")
for p in projects:
    if "Python" in p["technologies"]:
        print(p["project_name"])
python_projects = list(filter(lambda x: "Python" in x["technologies"], projects))
print("Using filter:", [p["project_name"] for p in python_projects])
# TASK 6
print("\n6. Total Budget:")
total = sum(p["budget"] for p in projects)
print(total)
# TASK 7
print("\n7. All Technologies in one list:")
all_techs = []
for p in projects:
    all_techs.extend(p["technologies"])
print(all_techs)
# TASK 8
print("\n8. Unique Technologies:")
unique_techs = set(all_techs)
print(unique_techs)
# TASK 9
print("\n9. Every Team Member:")
for p in projects:
    print(f"\nProject: {p['project_name']}")
    for member in p["team"]:
        print(f"  Name: {member['name']}, Role: {member['role']}, Exp: {member['experience']}")
# TASK 10
print("\n10. Members with >3 years exp:")
for p in projects:
    for member in p["team"]:
        if member["experience"] > 3:
            print(f"{member['name']} ({p['project_name']}) - {member['experience']} years")
# TASK 11
print("\n11. Total Team Members:")
count = sum(len(p["team"]) for p in projects)
print(count)
# TASK 12
print("\n12. Sorted by Budget (High to Low):")
by_budget = sorted(projects, key=lambda x: x["budget"], reverse=True)
for p in by_budget:
    print(p["project_name"], "-", p["budget"])
# TASK 13
print("\n13. Sorted by Project Name:")
by_name = sorted(projects, key=lambda x: x["project_name"])
for p in by_name:
    print(p["project_name"])
# TASK 14
print("\n14. Team Members Sorted by Experience:")
for p in projects:
    print(f"\nProject: {p['project_name']}")
    sorted_team = sorted(p["team"], key=lambda x: x["experience"])
    for member in sorted_team:
        print(f"  {member['name']} - {member['experience']} years")
