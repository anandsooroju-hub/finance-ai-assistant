import re

from src.llm.llm_client import generate
from src.llm.sql_prompt import build_sql_prompt
from src.database.sql_rules import validate_sql
from src.database.snowflake_connection import get_connection
from src.llm.response_generator import generate_business_response


def clean_sql(sql: str) -> str:
    """
    Remove markdown code fences that an LLM may add
    around otherwise valid SQL.
    """

    sql = sql.strip()

    sql = re.sub(
        r"^```sql\s*",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"^```\s*",
        "",
        sql
    )

    sql = re.sub(
        r"\s*```$",
        "",
        sql
    )

    return sql.strip()


def execute_governed_query(question: str):

    print("\nUSER QUESTION:")
    print(question)

    # -----------------------------
    # 1. Build LLM prompt
    # -----------------------------

    prompt = build_sql_prompt(question)

    # -----------------------------
    # 2. Generate candidate SQL
    # -----------------------------

    sql = generate(prompt).strip()

    # Normalize LLM output
    sql = clean_sql(sql)

    print("\nGENERATED SQL:")
    print(sql)

    # -----------------------------
    # 3. Validate SQL
    # -----------------------------

    valid, message = validate_sql(sql)

    print("\nVALIDATION:")
    print(message)

    if not valid:
        print("\nQUERY REJECTED.")
        return

    # -----------------------------
    # 4. Execute approved SQL
    # -----------------------------

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        print("\nSNOWFLAKE RESULT:")

        for row in rows:
            print(row)

        # -----------------------------
        # 5. Generate business response
        # -----------------------------

        answer = generate_business_response(
            question,
            rows
        )

        print("\nBUSINESS RESPONSE:")
        print(answer)

    finally:
        conn.close()


if __name__ == "__main__":

    question = "What was APAC revenue in Q2 2026?"

    execute_governed_query(question)
