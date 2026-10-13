class Employee:
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary

e1 = Employee(emp_id=101, name="Aman", department="IT", salary=75000)
e2 = Employee(emp_id=102, name="Sara", department="HR", salary=65000)
