import pandas as pd
df = pd.read_csv("orders.csv")
#Ex 1
print(
    df["status"].value_counts()
)
#Ex 2
result = (
    df.groupby("status")
    .size()
)
#string to date
df["order_date"] = pd.to_datetime(
    df["order_date"]
)
df["month"] = df["order_date"].dtmonth
print(df)