import os

import httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:20b-cloud")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")


class OllamaError(RuntimeError):
    pass


async def chat(system_prompt: str, user_prompt: str) -> str:
    base_url = OLLAMA_BASE_URL.rstrip("/")
    chat_url = f"{base_url}/chat" if base_url.endswith("/api") else f"{base_url}/api/chat"
    headers = {"Authorization": f"Bearer {OLLAMA_API_KEY}"} if OLLAMA_API_KEY else None

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
            response = await client.post(chat_url, json=payload, headers=headers)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise OllamaError(f"Ollama request failed: {exc}") from exc

    data = response.json()
    content = data.get("message", {}).get("content")
    if not isinstance(content, str) or not content.strip():
        raise OllamaError("Ollama response missing message content")
    return content.strip()
