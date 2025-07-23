from langgraph_sdk import get_client
from langchain_core.messages import convert_to_messages
from langchain_core.messages import HumanMessage, SystemMessage
import asyncio
import json
import asyncio
from typing import Dict
##from IPython.display import display, Markdown
from langchain.schema import HumanMessage
from src.retrieval_graph.graph import graph 
from langgraph.graph import END, START, StateGraph
with open('iscc_data.json', 'r') as f:
    input_data = json.load(f)
from src.retrieval_graph.graph import graph
#from IPython.display import display, Image
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
import asyncio
from IPython.display import display, Markdown
from dotenv import load_dotenv
load_dotenv()

async def main():
    # Create thread

    config = {"configurable": {"user_id": "Test","thread_id" :"1","query_model": "openai/gpt-4.1-nano","response_model": "openai/gpt-4.1-nano"}}
    graph_name = "retrieval_graph" 

    # Initial run
    async for chunk in graph.astream(  
        input={"input_data":input_data },
        config=config,
        interrupt_before=["human_edit"],
        stream_mode="messages-tuple"
    ):
        print("==="*25)
        # print(chunk)
        if chunk.event == "messages":
            print("".join(data_item['content'] for data_item in chunk.data if 'content' in data_item), end="", flush=True)
    print("hello world")
    graph.update_state(config, {"human_messages":[{"content":"satisfied"}] })
    async for chunk in graph.astream(
            input=None,
            config=config,
            interrupt_before=["human_edit"],
            stream_mode="messages-tuple"
        ):
            if chunk.event == "messages":
                print("".join(data_item['content'] for data_item in chunk.data if 'content' in data_item), end="", flush=True)

    # # Editing loop
    # while True:
    #     # Get the current thread state
    #     thread_state = "1"

    #     # Get current human messages
    #     current_human_messages = thread_state['values'].get('human_messages', [])

    #     # Prompt for user input
    #     print("\nPlease provide feedback or type 'satisfied' to complete editing:")
    #     user_input = await asyncio.to_thread(input, "Your input: ")

    #     # Check for satisfaction condition
    #     if "satisfied" in user_input.lower():
    #         break

    #     # Create a new human message as a string not as HumanMessage
    #     new_human_message = {
    #         "content": user_input,
    #         "role": "human"
    #     }

    #     # Append the new human message to the existing list
    #     updated_human_messages = current_human_messages + [new_human_message]

    #     # Prepare the update for the thread state
    #     update_input = {
    #         "human_messages": updated_human_messages  # Updated list of messages
    #     }

    #     # Update the thread state
    #     forked_config = await client.threads.update_state(
    #         thread["thread_id"],
    #         update_input
    #     )

    #     # Continue the run with the updated state
    #     async for chunk in graph.astream(
    #         thread["thread_id"], 
    #         graph_name, 
    #         input=None,
    #         config=config,
    #         checkpoint_id=forked_config['checkpoint_id'],
    #         interrupt_before=["human_edit"],
    #         stream_mode="messages-tuple"
    #     ):
    #         if chunk.event == "messages":
    #             print("".join(data_item['content'] for data_item in chunk.data if 'content' in data_item), end="", flush=True)

    # print("Editing process completed.")
asyncio.run(main())

# async def generate_report(iscc_dict: Dict, graph: StateGraph, input_data: Dict) -> str:
#     """Generates a report based on the provided ISCC dictionary and graph."""

#     # Set the initial state of the graph.
#     initial_state = {
#         'formatted_document': '',
#         'input_data': input_data
#     }

#     # Invoke the graph to generate the report.
#     result = await graph.ainvoke(initial_state)

#     # Extract the report from the graph's output.
#     formatted_document = result['formatted_document']

#     # Return the generated report.
#     return formatted_document

# # Sample Usage
# async def main():
#     report = await generate_report(input_data, graph, input_data)
#     display(Markdown(report))

# asyncio.run(main())