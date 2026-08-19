import sqlite3

from src.llm.ollama_client import ask_llama
from src.llm.sql_prompt import build_sql_prompt
from src.database.sql_rules import validate_sql
from src.llm.response_generator import generate_business_response


DB_PATH = "data/finance.db"


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

    sql = ask_llama(prompt).strip()

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

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.execute(sql)

        rows = cursor.fetchall()

        print("\nDATABASE RESULT:")

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