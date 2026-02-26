from dataclasses import dataclass, field
from langchain_openai import ChatOpenAI

import agent.config as config
from agent.context import Context

from langchain.agents.structured_output import ToolStrategy

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from agent.format import ResponseFormat
from agent.tools import register_age, register_age_from_date, register_goal, register_name


llm = ChatOpenAI(model_name=config.OPENAI_MODEL, temperature=config.TEMPERATURE)
tools = [register_name, register_age, register_goal, register_age_from_date]
checkpointer = InMemorySaver()

agent = create_agent(
    model=llm,
    system_prompt=config.SYSTEM_PROMPT,
    tools=tools,
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

def show_summary(context: Context) -> str:
    return (
        f"\nResumen final:\n"
        f"Nombre: {context.name}\n"
        f"Edad: {context.age}\n"
        f"Objetivo: {context.goal}"
    )
    
def chat_with_llm(session_id: str, msg: str, context: Context) -> ResponseFormat:
    llm_config = {"configurable": {"thread_id": session_id}}
    response = agent.invoke(
        {"messages": [{"role": "user", "content": msg}]},
        config=llm_config,
        context=context
    )
    
    return response['structured_response']

if __name__ == "__main__":
    session_context = Context()
    session_id = "session_1"

    print("=== Bienvenido al chat con el agente ===")
    print("El agente hará 3 preguntas y finalizará automáticamente cuando se respondan todas.\n")

    while not (session_context.name and session_context.age and session_context.goal):
        print("CONTEXT SUMMARY", session_context)
        user_msg = input("Tú: ").strip()
        llm_response = chat_with_llm(session_id, user_msg, session_context)
        print(f"Agente: {llm_response}\n")

    print(show_summary(session_context))
    print("\n=== Sesión finalizada ===")
