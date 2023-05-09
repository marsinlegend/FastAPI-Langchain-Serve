from typing import List

from helper import (
    CustomTool,
    PredefinedTools,
    get_agent,
    get_tools,
)
from langchain.callbacks import CallbackManager
from langchain.chat_models import ChatOpenAI

from lcserve import serving


@serving(websocket=True)
async def autogpt(
    name: str,
    role: str,
    goals: List[str],
    predefined_tools: PredefinedTools = None,
    custom_tools: List[CustomTool] = None,
    human_in_the_loop: bool = False,
    **kwargs,
) -> str:
    websocket = kwargs["websocket"]
    streaming_handler = kwargs['streaming_handler']

    llm = ChatOpenAI(
        temperature=0,
        verbose=True,
        streaming=True,
        callback_manager=CallbackManager([streaming_handler]),
    )
    tools = get_tools(llm, predefined_tools, custom_tools)
    agent = get_agent(
        name=name,
        role=role,
        websocket=websocket,
        tools=tools,
        llm=llm,
        human_in_the_loop=human_in_the_loop,
    )
    return await agent.arun(goals)
