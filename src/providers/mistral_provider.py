import os
import json
from mistralai.client import Mistral
from .base import LLMProvider


class MistralProvider(LLMProvider):
    def __init__(self):
        super().__init__(name="mistral")

        api_key = os.getenv("MISTRAL_API_KEY")
        model = os.getenv("MISTRAL_MODEL")

        if not api_key:
            raise RuntimeError("Missing MISTRAL_API_KEY in .env")
        if not model:
            raise RuntimeError("Missing MISTRAL_MODEL in .env")

        self.client = Mistral(api_key=api_key)
        self.model = model.strip()

    def generate_json(self, prompt: str) -> dict:
        resp = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        if not content:
            raise RuntimeError("Mistral returned empty JSON response.")
        return json.loads(content)

    def generate_text(self, prompt: str) -> str:
        resp = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = resp.choices[0].message.content
        if not content:
            raise RuntimeError("Mistral returned empty text response.")
        return content.strip()