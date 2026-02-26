from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "error": "Input inválido",
            "message": "Por favor envía un JSON con 'session_id' y 'message' ambos como texto no vacío."
        },
    )
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "error": "Error en la solicitud",
            "message": str(exc)
        },
    )
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "error": "Error interno del servidor",
            "message": "Ocurrió un error inesperado. Intenta nuevamente más tarde."
        },
    )

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
