from src.database.semantic_model import SEMANTIC_MODEL

REVENUE_EXPRESSION = SEMANTIC_MODEL["measures"]["revenue"]["expression"]


def build_sql_prompt(question: str, intent: dict) -> str:

    semantic_context = f"""
MEASURES:

{SEMANTIC_MODEL["measures"]}

DIMENSIONS:

{SEMANTIC_MODEL["dimensions"]}

TIME LOGIC:

{SEMANTIC_MODEL["time_logic"]}
"""

    intent_context = f"""
INTENT EXTRACTED FROM USER QUESTION:

{intent}

IMPORTANT:
Generate SQL based on this intent.
Do NOT infer filters or dimensions from examples.
The extracted intent is authoritative.
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

4. REVENUE IS A MEASURE.

   Whenever the user asks for revenue, total revenue,
   revenue generated, or revenue amount:

   ALWAYS use:

   COALESCE(SUM(f.REVENUE), 0)

   NEVER use:

   SUM(f.REVENUE)

   NEVER use:

   f.REVENUE

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

10. QUARTER DEFINITIONS ARE STRICT.

    Q1 means ALL dates from January 1 through March 31.
    Q2 means ALL dates from April 1 through June 30.
    Q3 means ALL dates from July 1 through September 30.
    Q4 means ALL dates from October 1 through December 31.

    NEVER interpret a quarter as a single month.

11. For date ranges, prefer inclusive/exclusive
    boundaries.

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

16. When the user asks for results "by" a dimension:

    - SELECT the dimension attribute.
    - GROUP BY the dimension attribute.
    - Do NOT filter to a specific dimension value
      unless the user explicitly provides one.

    Example:

    "What was revenue by region in Q1 2026?"

    MUST return revenue separately for each region.

INTENT CONTEXT:

{intent_context}

SEMANTIC CONTEXT:

{semantic_context}

USER QUESTION:

{question}

SQL:
"""

    return prompt