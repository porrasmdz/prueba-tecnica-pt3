from dataclasses import dataclass


@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    response: str
    is_finished: bool | None = False
    summary: str | None = None