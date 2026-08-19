from src.llm.ollama_client import ask_llama


def generate_business_response(
    question: str,
    sql_result
) -> str:

    prompt = f"""
You are a finance data assistant.

Answer the user's question using ONLY the supplied database result.

Do not invent information.

User question:
{question}

Database result:
{sql_result}

Provide a concise business-friendly answer.
"""


    return ask_llama(prompt)