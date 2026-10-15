def calculate_cost_per_kg(cost, weight):
    if weight <= 0:
        return 0
    return cost / weight
def classify_weight(weight):
    if weight > 20:
        return "Heavy"
    elif weight >= 10:
        return "Medium"
    else:
        return "Light"
def calculate_shipping_cost(weight, rate=50):
    return weight * rate
def get_shipment_category(weight):
    return classify_weight(weight)
def add_express_surcharge(cost, surcharge=200):
    return cost + surcharge