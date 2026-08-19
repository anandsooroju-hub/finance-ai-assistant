import sqlite3

conn = sqlite3.connect("data/finance.db")

query = """
SELECT
    f.year,
    f.quarter,
    r.region_name,
    SUM(f.revenue) AS total_revenue
FROM fact_revenue f
JOIN dim_region r
    ON f.region_id = r.region_id
WHERE r.region_name = 'APAC'
GROUP BY
    f.year,
    f.quarter,
    r.region_name
ORDER BY
    f.year,
    f.quarter;
"""

result = conn.execute(query).fetchall()

print("\nAPAC Revenue by Quarter")
print("-" * 40)

for row in result:
    print(row)

conn.close()