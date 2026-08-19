import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/finance.db")

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# -----------------------------
# Dimension: Client
# -----------------------------

clients = pd.DataFrame([
    (1, "Alpha Capital"),
    (2, "Beta Investments"),
    (3, "Gamma Asset Management"),
    (4, "Delta Bank"),
    (5, "Epsilon Partners"),
], columns=["client_id", "client_name"])

clients.to_sql(
    "dim_client",
    conn,
    if_exists="replace",
    index=False
)

# -----------------------------
# Dimension: Region
# -----------------------------

regions = pd.DataFrame([
    (1, "APAC"),
    (2, "EMEA"),
    (3, "Americas"),
], columns=["region_id", "region_name"])

regions.to_sql(
    "dim_region",
    conn,
    if_exists="replace",
    index=False
)

# -----------------------------
# Dimension: Product
# -----------------------------

products = pd.DataFrame([
    (1, "Equities"),
    (2, "Fixed Income"),
    (3, "Derivatives"),
], columns=["product_id", "product_name"])

products.to_sql(
    "dim_product",
    conn,
    if_exists="replace",
    index=False
)

# -----------------------------
# Fact: Revenue
# -----------------------------

revenue = pd.read_csv("data/finance_revenue.csv")

revenue.to_sql(
    "fact_revenue",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print(f"Database created successfully: {DB_PATH}")
print("Tables created:")
print(" - dim_client")
print(" - dim_region")
print(" - dim_product")
print(" - fact_revenue")