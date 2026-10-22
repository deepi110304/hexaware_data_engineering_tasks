def calculate_order_total(price, quantity):
    return price * quantity
def calculate_discount(amount):
    if amount >= 50000:
        return amount * 0.10
    else:
        return amount * 0.05
def check_stock(stock):
    if stock > 20:
        return "High Stock"
    elif stock >= 1:
        return "Low Stock"
    else:
        return "Out of Stock"