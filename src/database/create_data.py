import pandas as pd
from pathlib import Path

output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

clients = [
    (1, "Alpha Capital"),
    (2, "Beta Investments"),
    (3, "Gamma Asset Management"),
    (4, "Delta Bank"),
    (5, "Epsilon Partners"),
]

regions = [
    (1, "APAC"),
    (2, "EMEA"),
    (3, "Americas"),
]

products = [
    (1, "Equities"),
    (2, "Fixed Income"),
    (3, "Derivatives"),
]

dates = [
    (2026, "Q1"),
    (2026, "Q2"),
]

records = []

for year, quarter in dates:
    for client_id, client_name in clients:
        for region_id, region_name in regions:
            for product_id, product_name in products:

                base_revenue = (
                    client_id * 100000
                    + region_id * 50000
                    + product_id * 25000
                )

                if quarter == "Q2":
                    if region_name == "APAC":
                        revenue = base_revenue * 1.15
                    else:
                        revenue = base_revenue * 1.05
                else:
                    revenue = base_revenue

                cost = revenue * 0.65
                profit = revenue - cost

                records.append([
                    year,
                    quarter,
                    client_id,
                    region_id,
                    product_id,
                    revenue,
                    cost,
                    profit
                ])

df = pd.DataFrame(
    records,
    columns=[
        "year",
        "quarter",
        "client_id",
        "region_id",
        "product_id",
        "revenue",
        "cost",
        "profit"
    ]
)

df.to_csv(output_dir / "finance_revenue.csv", index=False)

print(f"Created {len(df)} finance records.")
print(f"File: {output_dir / 'finance_revenue.csv'}")