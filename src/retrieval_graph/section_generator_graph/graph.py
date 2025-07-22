"""Researcher graph used in the conversational retrieval system as a subgraph.

This module defines the core structure and functionality of the researcher graph,
which is responsible for generating search queries and retrieving relevant documents.
"""

from typing import TypedDict, cast, Dict

from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from src.retrieval_graph.configuration import AgentConfiguration
from src.retrieval_graph.section_generator_graph.state import QueryState, ResearcherState
from src.shared import retrieval
from src.retrieval_graph.state import InputState, AgentState
from src.shared.utils import load_chat_model


# async def generate_queries(
#     state: ResearcherState, *, config: RunnableConfig
# ) -> dict[str, list[str]]:
#     """Generate search queries based on the question (a step in the research plan).

#     This function uses a language model to generate diverse search queries to help answer the question.

#     Args:
#         state (ResearcherState): The current state of the researcher, including the user's question.
#         config (RunnableConfig): Configuration with the model used to generate queries.

#     Returns:
#         dict[str, list[str]]: A dictionary with a 'queries' key containing the list of generated search queries.
#     """

#     class Response(TypedDict):
#         queries: list[str]

#     configuration = AgentConfiguration.from_runnable_config(config)
#     model = load_chat_model(configuration.query_model).with_structured_output(Response)
#     messages = [
#         {"role": "system", "content": configuration.generate_queries_system_prompt},
#         {"role": "human", "content": state.question},
#     ]
#     response = cast(Response, await model.ainvoke(messages))
#     return {"queries": response["queries"]}


# async def retrieve_documents(
#     state: QueryState, *, config: RunnableConfig
# ) -> dict[str, list[Document]]:
#     """Retrieve documents based on a given query.

#     This function uses a retriever to fetch relevant documents for a given query.

#     Args:
#         state (QueryState): The current state containing the query string.
#         config (RunnableConfig): Configuration with the retriever used to fetch documents.

#     Returns:
#         dict[str, list[Document]]: A dictionary with a 'documents' key containing the list of retrieved documents.
#     """
#     with retrieval.make_retriever(config) as retriever:
#         response = await retriever.ainvoke(state.query, config)
#         return {"documents": response}


# def retrieve_in_parallel(state: ResearcherState) -> list[Send]:
#     """Create parallel retrieval tasks for each generated query.

#     This function prepares parallel document retrieval tasks for each query in the researcher's state.

#     Args:
#         state (ResearcherState): The current state of the researcher, including the generated queries.

#     Returns:
#         Literal["retrieve_documents"]: A list of Send objects, each representing a document retrieval task.

#     Behavior:
#         - Creates a Send object for each query in the state.
#         - Each Send object targets the "retrieve_documents" node with the corresponding query.
#     """
#     return [
#         Send("retrieve_documents", QueryState(query=query)) for query in state.queries
#     ]

#Node: Generate Introduction
async def generate_introduction(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    node_introduction_prompt = configuration.introduction_prompt.format(input_data = state.input_data)
    messages = [{"role": "system", "content": node_introduction_prompt}]
    response = await model.ainvoke(messages)
    state.sections["Introduction"] = response.content
    return {"sections": state.sections}

#generate calc methodology
async def generate_calculation_methodology(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the calculation methodology section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    prompt = configuration.calculation_methodology_prompt.format(input_data=state.input_data)
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["Calculation Methodology"] = response.content
    return {"sections": state.sections}

async def generate_allocation_approach(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the allocation approach section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    prompt = configuration.allocation_approach_prompt.format(input_data=state.input_data)
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["Allocation Approach"] = response.content
    return {"sections": state.sections}

async def generate_scope_of_analysis(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the scope of the analysis section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    # Defensive check
    if "General Information and data preparation" not in state.input_data:
        raise KeyError(
            f"Missing 'General Information and data preparation' in input_data. "
            f"Available keys: {list(state.input_data.keys())}. "
            "Check your input data structure."
        )
    prompt = configuration.scope_of_analysis_prompt.format(input_data=state.input_data)
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["Scope of the Analysis"] = response.content
    return {"sections": state.sections}

async def generate_activity_data_used(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the data used section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    prompt = configuration.activity_data_used_prompt.format(input_data=state.input_data["Company specific data"])
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["Activity Data Used"] = response.content
    return {"sections": state.sections}
async def generate_standard_data_used(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the data used section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    prompt = configuration.standard_data_used_prompt.format(input_data=state.input_data["standardData"])
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["Standard Data Used"] = response.content
    return {"sections": state.sections}

async def generate_assumptions_and_limitations(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the assumptions and limitations section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    prompt = configuration.assumptions_and_limitations_prompt.format(input_data=state.input_data)
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["Assumptions and Limitations"] = response.content
    return {"sections": state.sections}

async def generate_results_and_interpretation(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the results and interpretation section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    prompt = configuration.results_and_interpretation_prompt.format(input_data=state.input_data["Emission"])
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["Results and Interpretation"] = response.content
    return {"sections": state.sections}

async def generate_conclusion(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the conclusion section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    prompt = configuration.conclusion_prompt.format(input_data=state.input_data)
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["Conclusion"] = response.content
    return {"sections": state.sections}

async def generate_references(state: AgentState, *, config: RunnableConfig) -> Dict[str, str]:
    """Generates the references section."""
    configuration = AgentConfiguration.from_runnable_config(config)
    model = load_chat_model(configuration.query_model)
    prompt = configuration.references_prompt.format(input_data=state.input_data)
    messages = [{"role": "system", "content": prompt}]
    response = await model.ainvoke(messages)
    state.sections["References"] = response.content
    return {"sections": state.sections}
# # Define the graph
# builder = StateGraph(ResearcherState)
# builder.add_node(generate_queries)
# builder.add_node(retrieve_documents)
# builder.add_edge(START, "generate_queries")
# builder.add_conditional_edges(
#     "generate_queries",
#     retrieve_in_parallel,  # type: ignore
#     path_map=["retrieve_documents"],
# )
# builder.add_edge("retrieve_documents", END)
# # Compile into a graph object that you can invoke and deploy.
# graph = builder.compile()
# graph.name = "ResearcherGraph"

# Create the graph
builder = StateGraph(AgentState, config_schema=AgentConfiguration)

# Add nodes
builder.add_node(generate_introduction)
builder.add_node(generate_calculation_methodology)
builder.add_node(generate_allocation_approach)
builder.add_node(generate_scope_of_analysis)
builder.add_node(generate_activity_data_used)
builder.add_node(generate_standard_data_used)
builder.add_node(generate_assumptions_and_limitations)
builder.add_node(generate_results_and_interpretation)
#builder.add_node(generate_conclusion)
builder.add_node(generate_references)


# Add edges to connect nodes
builder.add_edge(START, "generate_introduction")
builder.add_edge(START, "generate_calculation_methodology")
builder.add_edge(START, "generate_allocation_approach")
builder.add_edge(START, "generate_scope_of_analysis")
builder.add_edge(START, "generate_activity_data_used")
builder.add_edge(START, "generate_standard_data_used")
builder.add_edge(START, "generate_assumptions_and_limitations")
builder.add_edge(START, "generate_results_and_interpretation")
#builder.add_edge(START, "generate_conclusion")
builder.add_edge(START, "generate_references")

# Connect all write-up nodes to the assembly node
builder.add_edge("generate_introduction", END)
builder.add_edge("generate_calculation_methodology", END)
builder.add_edge("generate_allocation_approach", END)
builder.add_edge("generate_scope_of_analysis", END)
builder.add_edge("generate_activity_data_used", END)
builder.add_edge("generate_standard_data_used", END)
builder.add_edge("generate_assumptions_and_limitations", END)
builder.add_edge("generate_results_and_interpretation", END)
#builder.add_edge("generate_conclusion", END)
builder.add_edge("generate_references", END)

graph = builder.compile()
graph.name = "Section_generator_graph"
