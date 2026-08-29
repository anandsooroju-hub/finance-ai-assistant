import json

from src.llm.llm_client import generate


def parse_intent(question: str) -> dict:

    prompt = f"""
You are a finance query intent parser.

Extract the business intent from the user's question.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.

Allowed measures:
- revenue

Allowed dimensions:
- region
- client
- product

Identify:

- measure
- dimension
- filters
- year
- quarter

IMPORTANT RULES:

1. "by region" means:
   dimension = "region"

2. "by client" means:
   dimension = "client"

3. "by product" means:
   dimension = "product"

4. A specific value such as APAC, AMER, or EMEA
   is a FILTER value, not a dimension.

5. If a specific region is mentioned, use:
   "filters": {{
       "region": "APAC"
   }}

6. If no dimension is requested:
   dimension = null

7. If there are no filters:
   filters = {{}}

8. Extract the calendar year if provided.

9. Extract the quarter if provided:
   Q1, Q2, Q3, or Q4.

Examples:

Question:
What was APAC revenue in Q1 2026?

Return:
{{
    "measure": "revenue",
    "dimension": null,
    "filters": {{
        "region": "APAC"
    }},
    "year": 2026,
    "quarter": "Q1"
}}

Question:
What was revenue by region in Q1 2026?

Return:
{{
    "measure": "revenue",
    "dimension": "region",
    "filters": {{}},
    "year": 2026,
    "quarter": "Q1"
}}

Question:
Show revenue by product for 2026.

Return:
{{
    "measure": "revenue",
    "dimension": "product",
    "filters": {{}},
    "year": 2026,
    "quarter": null
}}

USER QUESTION:

{question}

JSON:
"""

    result = generate(prompt).strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:

        print("Invalid JSON returned by LLM:")
        print(result)

        raise


if __name__ == "__main__":

    question = "What was revenue by region in Q1 2026?"

    intent = parse_intent(question)

    print("\nINTENT:")
    print(json.dumps(intent, indent=4))