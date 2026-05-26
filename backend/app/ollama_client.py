import os

import httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:20b-cloud")


class OllamaError(RuntimeError):
    pass


async def chat(system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "options": {
            "temperature": 0.2,
            "num_predict": 350,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise OllamaError(f"Ollama request failed: {exc}") from exc

    data = response.json()
    content = data.get("message", {}).get("content")
    if not isinstance(content, str) or not content.strip():
        raise OllamaError("Ollama response missing message content")
    return content.strip()
