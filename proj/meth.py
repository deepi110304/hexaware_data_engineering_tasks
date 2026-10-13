class Product:
    name = ""
    price = 0
    def display(self):
        print(f"Product: {self.name}")
        print(f"Price: {self.price}")
p1 = Product()
p1.name = "Monitor"
p1.price = 18000
p1.display()