file = open('employees.txt', "r")
for line in file:
    print(line.strip())
file.close()
file = open("employees.txt", "a")
file.write("11,sarah,sales,68000\n")
file.close()