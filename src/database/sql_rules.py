import re


ALLOWED_TABLES = {
    "fact_revenue",
    "dim_region",
    "dim_client",
    "dim_product",
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
    # 3. Check referenced tables
    # -----------------------------------

    tables_found = set(
        re.findall(
            r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)",
            sql_clean,
            re.IGNORECASE
        )
    )

    invalid_tables = tables_found - ALLOWED_TABLES

    if invalid_tables:
        return False, (
            f"Unauthorized table(s): "
            f"{', '.join(sorted(invalid_tables))}"
        )

    return True, "SQL passed validation."


if __name__ == "__main__":

    test_queries = {

        "Valid query": """
            SELECT SUM(f.revenue)
            FROM fact_revenue f
            JOIN dim_region r
                ON f.region_id = r.region_id
            WHERE r.region_name = 'APAC';
        """,

        "Dangerous DELETE": """
            DELETE FROM fact_revenue;
        """,

        "Dangerous DROP": """
            DROP TABLE fact_revenue;
        """,

        "Unauthorized table": """
            SELECT *
            FROM employee_salary;
        """
    }

    for name, query in test_queries.items():

        valid, message = validate_sql(query)

        print(f"\n{name}")
        print(f"Valid: {valid}")
        print(f"Message: {message}")