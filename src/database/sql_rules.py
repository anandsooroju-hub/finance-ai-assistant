import re
from src.database.semantic_model import SEMANTIC_MODEL

ALLOWED_TABLES = {
    "FINANCE_DEV.CORE.FACT_SALES",
    "FINANCE_DEV.CORE.DIM_REGION",
    "FINANCE_DEV.CORE.DIM_CUSTOMER",
    "FINANCE_DEV.CORE.DIM_PRODUCT",
}


FORBIDDEN_OPERATIONS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
}


def validate_sql(sql: str) -> tuple[bool, str]:

    sql_clean = sql.strip().rstrip(";")
    sql_clean = re.sub(r"^```sql\s*", "", sql_clean, flags=re.IGNORECASE)
    sql_clean = re.sub(r"\s*```$", "", sql_clean)
    sql_clean = sql_clean.strip()
    sql_upper = sql_clean.upper()

    # -----------------------------------
    # 1. Only SELECT statements allowed
    # -----------------------------------

    if not sql_upper.startswith("SELECT"):
        return False, "Only SELECT queries are permitted."

    # -----------------------------------
    # 2. Block dangerous operations
    # -----------------------------------

    for operation in FORBIDDEN_OPERATIONS:

        pattern = rf"\b{operation}\b"

        if re.search(pattern, sql_upper):
            return False, f"Forbidden SQL operation detected: {operation}"

    # -----------------------------------
    # 3. Revenue governance
    # -----------------------------------

    if "F.REVENUE" in sql_upper:

        revenue_expression = (
            SEMANTIC_MODEL["measures"]["revenue"]["expression"]
            .upper()
        )

        if revenue_expression not in sql_upper:
            return False, (
                "Invalid revenue logic: "
                "REVENUE must use the approved semantic expression."
            )

        if "COALESCE(" not in sql_upper:
            return False, (
                "Invalid revenue logic: "
                "REVENUE must use COALESCE."
            )
    # -----------------------------------
    # 4. Find referenced tables
    # -----------------------------------

    table_matches = re.findall(
        r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_\.]*)",
        sql_upper,
        re.IGNORECASE
    )

    tables_found = set(table_matches)

    # -----------------------------------
    # 5. Check table authorization
    # -----------------------------------

    invalid_tables = tables_found - ALLOWED_TABLES

    if invalid_tables:
        return False, (
            "Unauthorized table(s): "
            + ", ".join(sorted(invalid_tables))
        )

    return True, "SQL passed validation."


if __name__ == "__main__":

    test_queries = {

        "Valid revenue query": """
            SELECT SUM(f.REVENUE)
            FROM FINANCE_DEV.CORE.FACT_SALES f
            JOIN FINANCE_DEV.CORE.DIM_REGION r
                ON f.REGION_KEY = r.REGION_KEY
            WHERE r.REGION_NAME = 'APAC'
              AND f.SALE_DATE >= '2026-04-01'
              AND f.SALE_DATE < '2026-07-01';
        """,

        "Dangerous DELETE": """
            DELETE FROM FINANCE_DEV.CORE.FACT_SALES;
        """,

        "Dangerous DROP": """
            DROP TABLE FINANCE_DEV.CORE.FACT_SALES;
        """,

        "Unauthorized table": """
            SELECT *
            FROM FINANCE_DEV.CORE.EMPLOYEE_SALARY;
        """,

        "Invalid revenue logic": """
        SELECT f.REVENUE
        FROM FINANCE_DEV.CORE.FACT_SALES f;
        """
    }

    for name, query in test_queries.items():

        valid, message = validate_sql(query)

        print(f"\n{name}")
        print(f"Valid: {valid}")
        print(f"Message: {message}")