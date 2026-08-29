from src.llm.ollama_client import ask_llama


def generate_business_response(
    question: str,
    sql_result,
    retrieved_context=None
) -> str:

    context_text = ""

    if retrieved_context:
        context_text = "\n\n".join(
            f"Source: {item['source']}\n{item['content']}"
            for item in retrieved_context
        )

    prompt = f"""
You are a finance data assistant.

Answer the user's question using the supplied Snowflake database result
and, where relevant, the retrieved business context.

IMPORTANT:
- Treat the database result as the source of truth for numerical values.
- Treat retrieved context only as supporting business context.
- Do not invent facts that are not present in either source.
- If the retrieved context does not explain something, say so.
- Keep the answer concise and business-friendly.

User question:
{question}

Snowflake database result:
{sql_result}

Retrieved business context:
{context_text if context_text else "No relevant business context was retrieved."}

Answer:
"""

    return ask_llama(prompt)
