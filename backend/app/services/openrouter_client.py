"""
OpenRouter client — wrap OpenAI SDK ให้ชี้ไปที่ OpenRouter
OpenRouter เป็น OpenAI-compatible อยู่แล้ว แค่เปลี่ยน base_url + key
"""
import os
from openai import OpenAI

# ค่า default ของ model — เปลี่ยนผ่าน env ได้
DEFAULT_MODEL = os.getenv(
    "DEFAULT_MODEL", "meta-llama/llama-3.3-70b-instruct:free"
)

# Models ที่ใช้บ่อยใน project — alias ไว้สำหรับเรียกง่าย
MODELS = {
    "llama": "meta-llama/llama-3.3-70b-instruct:free",
    "qwen": "qwen/qwen-2.5-72b-instruct:free",
    "deepseek": "deepseek/deepseek-r1:free",
}


def get_client() -> OpenAI:
    """สร้าง OpenAI client ที่ชี้ไปที่ OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY ยังไม่ตั้งค่า — ดูที่ backend/.env.example"
        )
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


def chat(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.7,
) -> str:
    """
    เรียก chat completion แบบง่าย
    ใช้: chat([{"role": "user", "content": "hello"}])
    """
    client = get_client()
    selected = MODELS.get(model, model) if model else DEFAULT_MODEL
    response = client.chat.completions.create(
        model=selected,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
