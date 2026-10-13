class Employee:
    def work(self):
        print("Employee is working")
class Developer(Employee):
    def code(self):
        print("Writing python code")
class Tester(Employee):
    def test(self):
        print("Testing application")