import pandas as pd
df = pd.read_csv("orders.csv")
print(df["product"])
print(
    df[
        ["order_id", "product", "amount"]
    ]
)
delivered = df.query("status == 'Delivered'")
print(delivered)
result = df.query("amount > 20000")
print(result)
