class Employee:
    def __init__(self, name,  salary):
        self.name = name
        self.salary = salary
    def display_employee(self):
        print(f"Name: {self.name}")
        print(f"Salary: {self.salary}")
class Developer(Employee):
    def write_code(self):
        print("Developer is writing code")
d1 = Developer(name="Deepika", salary=200000)
d1.display_employee()
d1.write_code()