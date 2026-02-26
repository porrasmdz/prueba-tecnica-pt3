# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agent.context import Context
from agent.agent import chat_with_llm, show_summary

app = FastAPI(title="Agente Conversacional")

sessions: dict[str, Context] = {}
class ChatRequest(BaseModel):
    session_id: str
    message: str
class ChatResponse(BaseModel):
    response: str
    is_final: bool
    summary: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    context = sessions.get(req.session_id)
    if not context:
        context = Context()
        sessions[req.session_id] = context

    agent_response = chat_with_llm(req.session_id, req.message, context)

    is_final = bool(context.name and context.age and context.goal)
    summary = show_summary(context) if is_final else None

    # del sessions[req.session_id] 

    return ChatResponse(
        response=agent_response.response,
        is_final=is_final,
        summary=summary
    )