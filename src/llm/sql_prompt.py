from src.database.semantic_model import SEMANTIC_MODEL


def build_sql_prompt(question: str) -> str:

    semantic_context = f"""
Available measures:

{SEMANTIC_MODEL["measures"]}

Available dimensions:

{SEMANTIC_MODEL["dimensions"]}
"""

    prompt = f"""
You are an enterprise finance SQL assistant.

Your job is to convert the user's business question
into a read-only SQL query.

IMPORTANT RULES:

1. Generate SELECT queries only.
2. Do not generate INSERT, UPDATE, DELETE, DROP,
   ALTER, TRUNCATE or other data-changing statements.
3. Use only the tables and columns provided in the schema.
4. Revenue means SUM(f.revenue).
5. Region must use dim_region.region_name.
6. Return ONLY SQL.
7. Do not provide explanations or markdown.

DATABASE TABLES:

fact_revenue:
- year
- quarter
- client_id
- region_id
- product_id
- revenue
- cost
- profit

dim_region:
- region_id
- region_name

dim_client:
- client_id
- client_name

dim_product:
- product_id
- product_name

SEMANTIC CONTEXT:

{semantic_context}

USER QUESTION:

{question}

SQL:
"""

    return prompt