from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class LLMProvider(ABC):
    name: str

    @abstractmethod
    def generate_json(self, prompt: str) -> dict:
        ...

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        ...