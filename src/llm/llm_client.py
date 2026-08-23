from src.llm.ollama_client import ask_llama


def generate(prompt: str) -> str:
    return ask_llama(prompt)