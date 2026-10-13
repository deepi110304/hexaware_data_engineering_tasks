class Employee:
    _department = "IT" # Protected Variable

e1 = Employee()
print(e1._department) # Works - IT

class Employee:
    __bonus = 10000 # Private

    def get_bonus(self): # Way 1: Method vazhiya access panna
        return self.__bonus

e1 = Employee()

# print(e1.__bonus) # Error varum

# Way 1: Getter method use pannu (Correct way)
print(e1.get_bonus()) # 10000

# Way 2: Name Mangling vazhiya (Python internal name)
print(e1._Employee__bonus) # 10000 - but ithu recommend panna maatom