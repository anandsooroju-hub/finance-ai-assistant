import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def ask_llama(prompt: str) -> str:

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]


if __name__ == "__main__":

    answer = ask_llama(
        "What is SQL? Answer in one short sentence."
    )

    print("\nLlama response:")
    print(answer)