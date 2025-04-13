# # from langchain_core.tools import tool

# # @tool
# # def get_weather(city: str) -> str:
# #     """Get the weather in a specific city."""
# #     return f"The weather in {city} is sunny with 27°C."
# # from langchain_groq import ChatGroq

# # llm = ChatGroq(model="llama3-8b-8192", temperature=0)

# # # Bind the tools
# # runnable = llm.bind_tools(
# #     tools=[get_weather],
# #     tool_choice="auto",  # "any" to enforce tool usage, or specify tool name
# # )
# # from langchain_core.messages import HumanMessage

# # response = runnable.invoke([HumanMessage(content="What's the weather in Delhi?")])
# # print(response)

# from typing import Annotated
# from typing_extensions import TypedDict
# from langgraph.graph.message import add_messages
# from langgraph.graph import StateGraph
# from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_core.messages import HumanMessage
# from langchain_core.tools import tool
# from langchain_groq import ChatGroq  # or your chosen Groq-compatible model
# from importlib import import_module
# import os

# # Dynamically load all tools
# def load_tools():
#     tools = []
#     tool_dir = "tools"
#     for file in os.listdir(tool_dir):
#         if file.endswith(".py"):
#             mod = import_module(f"{tool_dir}.{file[:-3]}")
#             for attr in dir(mod):
#                 if callable(getattr(mod, attr)) and not attr.startswith("_"):
#                     tools.append(tool()(getattr(mod, attr)))
#     return tools

# llm = ChatGroq(model="llama3-8b-8192")  # You can switch to other models Groq supports

# tool_node = ToolNode(tools=load_tools())

# # Define the state graph
# # builder = StateGraph()
# class State(TypedDict):
#     messages: list
    
# builder = StateGraph(State)
# builder.set_entry_point("chat")
# builder.add_node("chat", llm.bind_tools(tools=load_tools(), tool_choice="auto"))
# builder.add_conditional_edges("chat", tools_condition)
# builder.add_node("tools", tool_node)
# builder.add_edge("tools", "chat")

# # Compile
# app = builder.compile()

# # Run
# while True:
#     query = input("You: ")
#     if query.lower() in ["exit", "quit"]:
#         break
#     result = app.invoke(HumanMessage(content=query))
#     print("Jarvis:", result)

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import tool

from langchain_groq import ChatGroq


# -------------------- 1. Define Tools --------------------

@tool
def get_time() -> str:
    """Returns the current time in 24-hour format as a string.

    Returns:
        str: The current time in 24-hour format, e.g. "14:30:00".
    """
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

@tool
def greet_user(name: str) -> str:
    """Greets a user by name and asks how it can assist them.
    
    Args:
        name (str): The user's name.

    Returns:
        str: A greeting message addressed to the user.
    """

    return f"Hello, {name}! How can I assist you today?"

@tool
def add_numbers(a: int, b: int) -> int:
    
    """Adds two numbers together.

    Args:
        a (int): The first number to add.
        b (int): The second number to add.

    Returns:
        int: The sum of the two input numbers.
    """
    return a + b

# Register all tools
tools = [get_time, greet_user, add_numbers]


# -------------------- 2. Setup Groq LLM --------------------

llm = ChatGroq(
    model_name="llama3-70b-8192",  # or "llama3-70b-8192"
    # groq_api_key="your-groq-api-key",  # <-- Replace with your actual key
    temperature=0,
    tools=tools
)


# -------------------- 3. Define State Functions --------------------

def llm_node(state):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": messages + [response]}

# Use prebuilt ToolNode to handle tool calling
tool_node = ToolNode(tools=tools)

def tool_output_handler(state):
    messages = state["messages"]
    ai_msg = messages[-1]

    new_messages = messages.copy()

    for call in ai_msg.tool_calls:
        tool_result = tool_node.invoke(ai_msg)
        new_messages.append(ToolMessage(
            tool_call_id=call.id,
            content=str(tool_result)
        ))

    return {"messages": new_messages}


# -------------------- 4. Build LangGraph --------------------

# builder = StateGraph()builder = StateGraph(dict)

builder = StateGraph(dict)

builder.add_node("llm", llm_node)
builder.add_node("tools", tool_node)
builder.add_node("tool_output_handler", tool_output_handler)

builder.set_entry_point("llm")

builder.add_conditional_edges(
    "llm",
    tools_condition,
    {
        "tool": "tools",
        "__end__": END
    }
)

builder.add_edge("tools", "tool_output_handler")
builder.add_edge("tool_output_handler", "llm")

graph = builder.compile()


# -------------------- 5. Run Jarvis in Full Loop --------------------

if __name__ == "__main__":
    print("🧠 Jarvis (Groq + LangGraph) is running...\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Jarvis: Goodbye! 👋")
            break

        state = {"messages": [HumanMessage(content=user_input)]}
        print("\n🤖 Jarvis is thinking...\n")

        final_response = None
        for step in graph.stream(state):
            for key, value in step.items():
                messages = value["messages"]
                for msg in messages:
                    if isinstance(msg, AIMessage) and msg.content:
                        final_response = msg.content

        print(f"Jarvis: {final_response}\n")
