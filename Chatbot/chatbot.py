from typing import Annotated
from typing_extensions import TypedDict

# from langchain_anthropic import ChatAnthropic
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from NLP.Natural_Language_Processing import speak
from Chatbot.Chroma_db import save_data, query_data
# from Milvus_db import save_data, query_data

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
graph_builder = StateGraph(State)

# ------------------------------------Tools------------------------------------
@tool
def search_vector_db(text: str):
    """if user asks something related to personal info, Search Vector DB for user details based on the given query text.Returns a list of related documents that match the query text to use as context.

    Args:
        text (str): The information query text required, to search for.
        
    Returns:
        documents (list): A list of related documents that match the query text to use as context.
    """
    res = query_data(query=text)
    print(res)
    return str(res)


@tool
def store_data(user_info: dict):
    """extract user info and provide as `user_info` argument to this function. Stores any new personal information (like name, location, interests, job, etc.) in a vector database.

    Args:
        user_info (dict): A dictionary containing one or more user's personal information as summarized as key-value pair.
        example: {"name": "John Doe", "location": "New York", "interests": ["reading", "hiking"]} or {"name": "John Doe"} only would be acceptible too.

    Returns:
        str: A message indicating whether the personal information was stored successfully.
    """
    # print('store_data:',user_info,type(user_info))
    # print(len(user_info))
    similar_data = query_data(query=str(user_info), top_k=len(user_info)+2)
    # print('similar_data:',similar_data)

    for key, value in user_info.items():
        user_data=str({key:value})
        
        if similar_data:
            for data in similar_data:
                # print(key)
                # print(data)
                # print(eval(data['id']))

                if key in eval(data['data']):
                    # print(data['id'])
                    res = save_data(data=user_data,id=data['id'])
                    if isinstance(res, ValueError):
                        return res
                    # print('updated ....')
                    break
            else:
                res = save_data(data=user_data)
                if isinstance(res, ValueError):
                    return res
                # print('saved....')
        else:
            res =save_data(data=user_data)
            if isinstance(res, ValueError):
                return res
            # print('saved....')


    # if not user_info:
    #     return "No personal data to store."

    # print(f"Storing personal data: {user_info}")

    return f"Personal info stored successfully: {user_info}, No need to tell user, just respond NORMALLY "


# travily_tool = TavilySearchResults(max_results=2)
tools_list = [search_vector_db,store_data]
# -----------------------------------------------------------------------------

# llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
# llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm = ChatGroq(model_name="llama3-70b-8192", temperature=0)

llm_with_tools = llm.bind_tools(tools_list)

# ------------------------------------Nodes------------------------------------
def chatbot(state: State):
    # print('bot:')
    state = {"messages": [llm_with_tools.invoke(state["messages"])]}
    # print('2')
    return state

def extract_info(state: State):
    """Extracts and saves user's personal and important details if present for future use."""
    messages = state["messages"]
    
    prompt = "Does the last message contain personal information like name, location, interests, job, etc? Reply with either 'yes' or 'no' only.No need to use any tools just reply logically."
    print('check:')
    response = llm_with_tools.invoke(messages + [SystemMessage(content=prompt)])
    if response.content.lower().startswith("yes"):
    # Ask LLM to check if there's personal info to extract
        print('extract:')
        prompt = "Extract any new personal information (like name, location, interests, job, etc.) in a python dict format from the latest message. If no personal info is found, return {}."
        response = llm_with_tools.invoke(messages + [SystemMessage(content=prompt)])

        extracted_data = response.content  # Assume LLM returns structured JSON
        print('data extracted',extracted_data)


    # if extracted_data:  # Store only if new personal info is found
    #     in_db = llm_with_tools.invoke(messages + [SystemMessage(content="Does the extracted data already exist in the vector database? Reply with either 'yes' or 'no' only.")])
    #     if not in_db:
    #         save_data(data=extracted_data)
    
    return state  # No update if no personal info is found


tool_node = ToolNode(tools=tools_list)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
# graph_builder.add_node("extract_info", extract_info)

# ------------------------------------Edges------------------------------------
def should_extract_info(state: State):
    """Determines if we should extract user details from the latest message."""
    
    messages = state["messages"]
    # print(messages)
    # return False
    # Ask LLM if the last message contains personal info
    prompt = "Does the last message contain personal information like name, location, interests, job, etc? Reply with either 'yes' or 'no' only."
    
    #  {"messages": [llm_with_tools.invoke(state["messages"])]}

    # graph.update_state(config,{"messages": response})
    print('check:')
    response = llm_with_tools.invoke(messages + [SystemMessage(content=prompt)])
    print('response:',response.content)
    # response = state
    return response.content.lower().startswith("yes")
# graph_builder.add_conditional_edges("chatbot", should_extract_info, {True: "extract_info",False:END})
# graph_builder.add_edge("extract_info", "chatbot")

# graph_builder.add_edge("chatbot", "extract_info")

# graph_builder.add_conditional_edges("extract_info", tools_condition)
# graph_builder.add_edge("tools", "extract_info")


graph_builder.add_conditional_edges("chatbot",tools_condition)
graph_builder.add_edge("tools", "chatbot")

graph_builder.set_entry_point("chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ChatBot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

config = {"configurable": {"thread_id": "1"}}
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]},config):
        print('event')
        for value in event.values():
            last_msg =f"Assistant: {value["messages"][-1].content}"
    print(last_msg)
    speak(text=last_msg)

while True:
    # try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    # except :
    #     print("No input provided. Please try again.")
    #     # # fallback if input() is not available
    #     # user_input = "What do you know about LangGraph?"
    #     # print("User: " + user_input)
    #     # stream_graph_updates(user_input)
    #     # break