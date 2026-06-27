import os
from anthropic import Anthropic
from .base import LLMProvider
from . import safe_json_load

class ClaudeProvider(LLMProvider):
    def __init__(self):
        super().__init__(name="claude")
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = os.getenv("ANTHROPIC_MODEL")

    def generate_json(self, prompt: str) -> dict:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0,
            system="Return a single JSON object and nothing else.",
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text
        return safe_json_load(text)

    def generate_text(self, prompt: str) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text