import re

from src.llm.llm_client import generate
from src.llm.sql_prompt import build_sql_prompt
from src.database.sql_rules import validate_sql
from src.database.snowflake_connection import get_connection
from src.llm.response_generator import generate_business_response
from src.rag.vector_retriever import retrieve_documents


def clean_sql(sql: str) -> str:
    """Remove markdown code fences that an LLM may add around SQL."""
    sql = sql.strip()
    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```\s*", "", sql)
    sql = re.sub(r"\s*```$", "", sql)
    return sql.strip()


def execute_governed_query(question: str):
    print("\nUSER QUESTION:")
    print(question)

    # 1. Retrieve relevant business context.
    retrieved = retrieve_documents(question, top_k=3)

    print("\nRETRIEVED CONTEXT:")
    for result in retrieved:
        print(f"- {result['source']} (score={result['score']:.4f})")

    # 2. Generate SQL from the authoritative semantic model.
    prompt = build_sql_prompt(question)
    sql = clean_sql(generate(prompt).strip())

    print("\nGENERATED SQL:")
    print(sql)

    # 3. Validate SQL before execution.
    valid, message = validate_sql(sql)

    print("\nVALIDATION:")
    print(message)

    if not valid:
        print("\nQUERY REJECTED.")
        return

    # 4. Execute approved SQL in Snowflake.
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        print("\nSNOWFLAKE RESULT:")
        for row in rows:
            print(row)

        # 5. Generate the final answer using both structured data and
        # retrieved business context. Snowflake remains the source of truth
        # for numerical results.
        answer = generate_business_response(
            question,
            rows,
            retrieved_context=retrieved
        )

        print("\nBUSINESS RESPONSE:")
        print(answer)

    finally:
        conn.close()


if __name__ == "__main__":
    question = "Why did APAC revenue increase in Q2 2026?"
    execute_governed_query(question)
