
from langchain.tools import tool, ToolRuntime
from datetime import datetime, date
from agent.context import Context
@tool
def register_name(user_answer: str, runtime: ToolRuntime[Context]) -> str:
    """Registra el nombre del usuario en el contexto."""
    runtime.context.name = user_answer
    return f"Nombre registrado: {user_answer}"

@tool
def register_age(age: int, runtime: ToolRuntime[Context]) -> str:
    """Registra la edad del usuario, en formato de número entero en el contexto."""
    runtime.context.age = age
    return f"Edad registrada: {age}"


@tool
def register_age_from_date(date_str: str, runtime: ToolRuntime[Context]) -> str:
    """
    Registra la edad del usuario en el contexto.
    user_answer debe ser una fecha en formato ISO: YYYY-MM-DD
    """
    try:
        birth_date = datetime.fromisoformat(date_str).date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        runtime.context.age = age
        return f"Edad registrada: {age} años"
    except ValueError:
        return "Formato de fecha inválido. Por favor usa YYYY-MM-DD."
    
@tool
def register_goal(user_answer: str, runtime: ToolRuntime[Context]) -> str:
    """Registra el objetivo principal del usuario en el contexto.
    El objetivo principal es una de las siguientes opciones:
        - perder peso
        - ganar músculo
        - mejorar resistencia.
    
    """
    runtime.context.goal = user_answer
    return f"Objetivo registrado: {user_answer}"
