
from dataclasses import dataclass, field


@dataclass
class Context:
    """User context and in-memory storage"""
    name: str | None = None
    age: str | None = None
    goal: str | None = None