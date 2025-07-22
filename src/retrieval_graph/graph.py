"""Main entrypoint for the conversational retrieval graph.

This module defines the core structure and functionality of the conversational
retrieval graph. It includes the main graph definition, state management,
and key functions for processing & routing user queries, generating research plans to answer user questions,
conducting research, and formulating responses.
"""
from langgraph.checkpoint.memory import MemorySaver
from typing import Any, Literal, TypedDict, cast, Dict
import json
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

from src.retrieval_graph.configuration import AgentConfiguration
from src.retrieval_graph.section_generator_graph.graph import graph as Section_generator_graph

from src.retrieval_graph.state import AgentState, InputState, Router
from src.shared.utils import format_docs, load_chat_model
#from IPython.display import display, Markdown
import asyncio
# this dict contains the keys as tab and in every value of the tab is the requireired information that is inputted from user or is predefined.

with open('iscc_data.json', 'r') as f:
    ISCC_DICT = json.load(f)
    
# ISCC_DICT = {"Guide":{"about":"This tool automatically calculates the greenhouse gas (GHG) intensity of corn as a biomass feedstock for producing transportation fuels according to the requirements of ISCC EU  and EU RED II regulation."},

#              "General Information and data preparation":{"general information":{"Analysis Period":" 1 year "},
#                                                          "Farm description":{"name":" Manish Corn Farm" , "location":" California, USA "},
#                                                          "Project Description":{"brief":" This is a corn farm and we need to grow best organic corn "}},

#              "Company specific data":{"Yeild":{"Corn Production":{"Amount":"12","Unit":"ton per hectare per year","Source":"enter source of input data","Notes":"AI reasoning"},

#                                                "Moisture Content":{"Amount":"15%","Unit":"%","Source":"enter source of input data","Notes":"add any notes"},
#                                                "Fraction of crop area burnt annually":{"Amount":"0","Unit":"hectare burnt per hectare total","Source":"enter source of input data","Notes":"add any notes"},
#                                                "Straw yield (removed from the yield)":{"Amount":"0","Unit":"kg dry matter per hectare per year","Source":"enter source of input data","Notes":"add any notes"},
#                                                "Soil Type acidic or basic":{"Amount":"acidic ","Unit":"N/A","Source":"enter source of input data","Notes":"add any notes"}},

#                                       "Liquid Fuel Consumption":{"Diesel":{"Amount":"12","Unit":"liter per hectare per year","Source":"enter source of input data","Notes":"add any notes"},
#                                                                  "Gasoline":{"Amount":"24","Unit":"liter per hectare per year","Source":"enter source of input data","Notes":"add any notes"},
#                                                                  "Heavy fuel oil":{"Amount":"2300%","Unit":"liter per hectare per year","Source":"enter source of input data","Notes":"add any notes"},
#                                                                  "Methanol":{"Amount":"4","Unit":"liter per hectare per year","Source":"enter source of input data","Notes":"add any notes"},
#                                                                  "Straw yield (removed from the yield)":{"Amount":"0","Unit":"kg dry matter per hectare per year","Source":"enter source of input data","Notes":"add any notes"},
#                                                                  "Soil Type acidic or basic":{"Amount":"acidic ","Unit":"N/A","Source":"enter source of input data","Notes":"add any notes"}},
#                                       "Gaseous Fuels Consumption":{"LPG":"20 MJ per hectare per year",
#                                                                    "Natural Gas (HHV)":"12 MJ per hectare per year"},
#                                       "Solid Fuels Consumption":{"Hard coal":" 5 kg per hectare per year",
#                                                                  "Liginite":"5 kg per hectare per year",
#                                                                  "wood chip":"7 kg per hectare per year",
#                                                                  "wood pellets":"2 kg per hectare per year"},
#                                       "Electricity":{"Grid Electricity ":"0 kWh per hectare per year"},
#                                       "Synthetic Nitrogen Fertilizers Consumption ":{},
#                                       "":{}},

#              "Emission":{"Cultivation Emission":{"Liquid Fluids":{"Diesel":{"CO2":"24.45 KG", "CH4":"0" , "N2O":"0" ,"CO2e":"24.45"},
#                                                                   "Gasoline":{"CO2":"24.45 KG", "CH4":"0" , "N2O":"0" ,"CO2e":"24.45"},
#                                                                   "Heavy Fuel Oil":{"CO2":"24.45 KG", "CH4":"0" , "N2O":"0" ,"CO2e":"24.45"},
#                                                                   "Methanol":{"CO2":"24.45 KG", "CH4":"0" , "N2O":"0" ,"CO2e":"24.45"}},
#                                                  "":{"":{},
#                                                      "":{},
#                                                      "":{}}},
#                          },

#              "Farming N2O emission":{},
#              "Acidification and lining emission":{}}
# async def analyze_and_route_query(
#     state: AgentState, *, config: RunnableConfig
# ) -> dict[str, Router]:
#     """Analyze the user's query and determine the appropriate routing.

#     This function uses a language model to classify the user's query and decide how to route it
#     within the conversation flow.

#     Args:
#         state (AgentState): The current state of the agent, including conversation history.
#         config (RunnableConfig): Configuration with the model used for query analysis.

#     Returns:
#         dict[str, Router]: A dictionary containing the 'router' key with the classification result (classification type and logic).
#     """
#     configuration = AgentConfiguration.from_runnable_config(config)
#     model = load_chat_model(configuration.query_model)
#     messages = [
#         {"role": "system", "content": configuration.router_system_prompt}
#     ] + state.messages
#     response = cast(
#         Router, await model.with_structured_output(Router).ainvoke(messages)
#     )
#     return {"router": response}


# def route_query(
#     state: AgentState,
# ) -> Literal["create_research_plan", "ask_for_more_info", "respond_to_general_query"]:
#     """Determine the next step based on the query classification.

#     Args:
#         state (AgentState): The current state of the agent, including the router's classification.

#     Returns:
#         Literal["create_research_plan", "ask_for_more_info", "respond_to_general_query"]: The next step to take.

#     Raises:
#         ValueError: If an unknown router type is encountered.
#     """
#     _type = state.router["type"]
#     if _type == "langchain":
#         return "create_research_plan"
#     elif _type == "more-info":
#         return "ask_for_more_info"
#     elif _type == "general":
#         return "respond_to_general_query"
#     else:
#         raise ValueError(f"Unknown router type {_type}")


# async def ask_for_more_info(
#     state: AgentState, *, config: RunnableConfig
# ) -> dict[str, list[BaseMessage]]:
#     """Generate a response asking the user for more information.

#     This node is called when the router determines that more information is needed from the user.

#     Args:
#         state (AgentState): The current state of the agent, including conversation history and router logic.
#         config (RunnableConfig): Configuration with the model used to respond.

#     Returns:
#         dict[str, list[str]]: A dictionary with a 'messages' key containing the generated response.
#     """
#     configuration = AgentConfiguration.from_runnable_config(config)
#     model = load_chat_model(configuration.query_model)
#     system_prompt = configuration.more_info_system_prompt.format(
#         logic=state.router["logic"]
#     )
#     messages = [{"role": "system", "content": system_prompt}] + state.messages
#     response = await model.ainvoke(messages)
#     return {"messages": [response]}


# async def respond_to_general_query(
#     state: AgentState, *, config: RunnableConfig
# ) -> dict[str, list[BaseMessage]]:
#     """Generate a response to a general query not related to LangChain.

#     This node is called when the router classifies the query as a general question.

#     Args:
#         state (AgentState): The current state of the agent, including conversation history and router logic.
#         config (RunnableConfig): Configuration with the model used to respond.

#     Returns:
#         dict[str, list[str]]: A dictionary with a 'messages' key containing the generated response.
#     """
#     configuration = AgentConfiguration.from_runnable_config(config)
#     model = load_chat_model(configuration.query_model)
#     system_prompt = configuration.general_system_prompt.format(
#         logic=state.router["logic"]
#     )
#     messages = [{"role": "system", "content": system_prompt}] + state.messages
#     response = await model.ainvoke(messages)
#     return {"messages": [response]}


# async def create_research_plan(
#     state: AgentState, *, config: RunnableConfig
# ) -> dict[str, list[str] | str]:
#     """Create a step-by-step research plan for answering a LangChain-related query.

#     Args:
#         state (AgentState): The current state of the agent, including conversation history.
#         config (RunnableConfig): Configuration with the model used to generate the plan.

#     Returns:
#         dict[str, list[str]]: A dictionary with a 'steps' key containing the list of research steps.
#     """

#     class Plan(TypedDict):
#         """Generate research plan."""

#         steps: list[str]

#     configuration = AgentConfiguration.from_runnable_config(config)
#     model = load_chat_model(configuration.query_model).with_structured_output(Plan)
#     messages = [
#         {"role": "system", "content": configuration.research_plan_system_prompt}
#     ] + state.messages
#     response = cast(Plan, await model.ainvoke(messages))
#     return {"steps": response["steps"], "documents": "delete"}


# async def conduct_research(state: AgentState) -> dict[str, Any]:
#     """Execute the first step of the research plan.

#     This function takes the first step from the research plan and uses it to conduct research.

#     Args:
#         state (AgentState): The current state of the agent, including the research plan steps.

#     Returns:
#         dict[str, list[str]]: A dictionary with 'documents' containing the research results and
#                               'steps' containing the remaining research steps.

#     Behavior:
#         - Invokes the researcher_graph with the first step of the research plan.
#         - Updates the state with the retrieved documents and removes the completed step.
#     """
#     result = await researcher_graph.ainvoke({"question": state.steps[0]})
#     return {"documents": result["documents"], "steps": state.steps[1:]}


# def check_finished(state: AgentState) -> Literal["respond", "conduct_research"]:
#     """Determine if the research process is complete or if more research is needed.

#     This function checks if there are any remaining steps in the research plan:
#         - If there are, route back to the `conduct_research` node
#         - Otherwise, route to the `respond` node

#     Args:
#         state (AgentState): The current state of the agent, including the remaining research steps.

#     Returns:
#         Literal["respond", "conduct_research"]: The next step to take based on whether research is complete.
#     """
#     if len(state.steps or []) > 0:
#         return "conduct_research"
#     else:
#         return "respond"


# async def respond(
#     state: AgentState, *, config: RunnableConfig
# ) -> dict[str, list[BaseMessage]]:
#     """Generate a final response to the user's query based on the conducted research.

#     This function formulates a comprehensive answer using the conversation history and the documents retrieved by the researcher.

#     Args:
#         state (AgentState): The current state of the agent, including retrieved documents and conversation history.
#         config (RunnableConfig): Configuration with the model used to respond.

#     Returns:
#         dict[str, list[str]]: A dictionary with a 'messages' key containing the generated response.
#     """
#     configuration = AgentConfiguration.from_runnable_config(config)
#     model = load_chat_model(configuration.response_model)
#     context = format_docs(state.documents)
#     prompt = configuration.response_system_prompt.format(context=context)
#     messages = [{"role": "system", "content": prompt}] + state.messages
#     response = await model.ainvoke(messages)
#     return {"messages": [response]}


# # Define the graph
# builder = StateGraph(AgentState, input=InputState, config_schema=AgentConfiguration)
# builder.add_node(analyze_and_route_query)
# builder.add_node(ask_for_more_info)
# builder.add_node(respond_to_general_query)
# builder.add_node(conduct_research)
# builder.add_node(create_research_plan)
# builder.add_node(respond)

# builder.add_edge(START, "analyze_and_route_query")
# builder.add_conditional_edges("analyze_and_route_query", route_query)
# builder.add_edge("create_research_plan", "conduct_research")
# builder.add_conditional_edges("conduct_research", check_finished)
# builder.add_edge("ask_for_more_info", END)
# builder.add_edge("respond_to_general_query", END)
# builder.add_edge("respond", END)

# # Compile into a graph object that you can invoke and deploy.
# graph = builder.compile()
# graph.name = "RetrievalGraph"

# Node: conduct_research

# Node: conduct_research

async def generate_sections(state: AgentState) -> dict[str, Any]:
  """ Execute the first step of the research plan.

  This function takes the first step from the research plan and uses it to conduct research.

  Args:
    state (AgentState): The current state of the agent, including the research plan steps.

  Returns:
    dict[str, list[str]]: A dictionary with 'documents' containing the research results and 'steps'
    containing the remaining steps of the research plan.

  Behavior:
   - Invokes the researcher_graph with the first step of the research plan.
   - Updates the state with the retrieved documents and removes the completed step.
  """
  initial_state = {
        'input_data': state.input_data
    }
  result = await Section_generator_graph.ainvoke({'input_data':state.input_data})
  return {"sections": result["sections"]}


async def assemble_and_format(state: AgentState, *, config: RunnableConfig) -> Dict[str,str]:
    """Assembles the sections and formats the document."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)

    try:
        # 1. Process sections
        # If sections contain dictionaries, extract the relevant text content
        processed_sections = {}
        for key, value in state.sections.items():
            if isinstance(value, dict):
                # Assuming the dictionary has a 'content' or 'text' field
                # Adjust these keys based on your actual dictionary structure
                content = value.get('content') or value.get('text') or str(value)
                processed_sections[key] = content
            elif isinstance(value, str):
                processed_sections[key] = value
            else:
                processed_sections[key] = str(value)

        # 2. Combine sections
        all_content = "\n".join(processed_sections.values())

        # 3. Prepare prompt for formatting
        # Use processed_sections instead of raw sections
        prompt = configuration.assembly_prompt.format(
            input_data=state.input_data,
            sections=processed_sections
        )

        # 4. Invoke model for formatting
        messages = [{"role": "system", "content": prompt}]
        response = await model.ainvoke(messages)
        formatted_content = response.content

        # 5. Store the formatted content
        state.formatted_document = formatted_content
        state.edited_document = formatted_content

        return state

    except Exception as e:
        print(f"Error in assemble_and_format: {str(e)}")
        print(f"Sections type: {type(state.sections)}")
        print(f"Sections content: {state.sections}")
        raise

async def human_edit(state:AgentState,*,config:RunnableConfig) -> Dict[str, str]:
  """"Allow the humans to edit the final response"""
  configuration = AgentConfiguration.from_runnable_config(config)
  model = load_chat_model(configuration.query_model)
  prompt = configuration.human_edit_prompt.format(
        formatted_document=state.formatted_document,
        sections=", ".join(state.sections.keys()),
        human_message = state.human_messages[-1]
    )

    # Invoke model to present the document for editing and apply edits
  messages = [{"role": "system", "content": prompt}]
  response = await model.ainvoke(messages)
  edited_document = response.content
  state.edited = edited_document
  #display(Markdown(state.edited))
  return {"edited": state.edited}

def human_edit_condition(state: AgentState, *, config: RunnableConfig) -> bool:
    """Check if the user is satisfied with the document."""
    # Assume the user expresses satisfaction by sending a message containing "satisfied"
    last_message = state.human_messages[-1] if state.human_messages else None
    #print(last_message)
    if last_message and "satisfied" in last_message["content"]:
        return False  # User is satisfied, exit loop
    return True  # User is not satisfied, continue loop


# Create the graph
builder = StateGraph(AgentState, input=InputState, config_schema=AgentConfiguration)

# Add nodes
builder.add_node(generate_sections)
builder.add_node(assemble_and_format)
builder.add_node(human_edit)

builder.add_edge(START,"generate_sections") # This line connects the START node to the "generate_sections" node.
builder.add_edge("generate_sections", "assemble_and_format")
builder.add_edge("assemble_and_format", "human_edit")  # Pass agent_state
builder.add_conditional_edges(
        "human_edit",  # Source node
        human_edit_condition,  # Condition function
        {
            True: "human_edit",  # Target node if True (loop back)
            False: END,  # Target node if False (proceed to END)
        },
    )
builder.add_edge("human_edit", END)  # Update agent_state
memory = MemorySaver()
# Compile the graph
graph = builder.compile(checkpointer=memory)
graph.name = "Report"
