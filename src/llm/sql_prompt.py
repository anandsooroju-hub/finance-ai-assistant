from src.database.semantic_model import SEMANTIC_MODEL


def build_sql_prompt(question: str) -> str:

    semantic_context = f"""
MEASURES:

{SEMANTIC_MODEL["measures"]}

DIMENSIONS:

{SEMANTIC_MODEL["dimensions"]}

TIME LOGIC:

{SEMANTIC_MODEL["time_logic"]}
"""

    prompt = f"""
You are an enterprise finance SQL assistant.

Convert the user's business question into
ONE read-only Snowflake SQL query.

IMPORTANT RULES:

1. Generate SELECT queries only.

2. Never generate:
   INSERT
   UPDATE
   DELETE
   DROP
   ALTER
   TRUNCATE
   CREATE
   GRANT
   REVOKE

3. Use ONLY these tables:

   FINANCE_DEV.CORE.FACT_SALES
   FINANCE_DEV.CORE.DIM_REGION
   FINANCE_DEV.CORE.DIM_CUSTOMER
   FINANCE_DEV.CORE.DIM_PRODUCT

4. REVENUE IS A MEASURE, NOT A COLUMN TO RETURN DIRECTLY.

   Whenever the user asks for revenue, total revenue,
   revenue generated, or revenue amount:

   ALWAYS use:

   COALESCE(SUM(f.REVENUE), 0)

   NEVER use:

   f.REVENUE

   Example:

   SELECT COALESCE(SUM(f.REVENUE), 0) AS TOTAL_REVENUE
   FROM FINANCE_DEV.CORE.FACT_SALES f

5. Region must use:

   r.REGION_NAME

6. Region join:

   f.REGION_KEY = r.REGION_KEY

7. Customer join:

   f.CUSTOMER_KEY = c.CUSTOMER_KEY

8. Product join:

   f.PRODUCT_KEY = p.PRODUCT_KEY

9. There is NO quarter column.

   Derive quarters from f.SALE_DATE.

10. Quarter boundaries are:

    Q1 = January 1 through March 31
    Q2 = April 1 through June 30
    Q3 = July 1 through September 30
    Q4 = October 1 through December 31

11. For date ranges, prefer inclusive/exclusive
    boundaries.

    Example:

    Q2 2026 means:

    f.SALE_DATE >= '2026-04-01'
    AND f.SALE_DATE < '2026-07-01'

12. Use table aliases:

    f = FACT_SALES
    r = DIM_REGION
    c = DIM_CUSTOMER
    p = DIM_PRODUCT

13. Fully qualify the table names.

14. Return ONLY SQL.
    No explanation.
    No markdown.
    No ```sql fences.

15. Only join dimensions required by the user's question.

   For a region + revenue question, DIM_REGION is required.

   DIM_CUSTOMER and DIM_PRODUCT must NOT be joined unless
   the user asks about customer or product.

SEMANTIC CONTEXT:

{semantic_context}

USER QUESTION:

{question}

SQL:
"""

    return prompt