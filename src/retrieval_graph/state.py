"""State management for the retrieval graph.

This module defines the state structures used in the retrieval graph. It includes
definitions for agent state, input state, and router classification schema.
"""

from dataclasses import dataclass, field
from typing import Annotated, Literal, TypedDict
from typing import Annotated, Literal, TypedDict, Dict, Any
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

from src.shared.state import reduce_docs


# Optional, the InputState is a restricted version of the State that is used to
# define a narrower interface to the outside world vs. what is maintained
# internally.
def merge_dicts(a, b):
    """Merges dictionary b into dictionary a."""
    a.update(b)  # Update a with content from b
    return a
@dataclass(kw_only=True)
class InputState:
    """Represents the input state for the agent.

    This class defines the structure of the input state, which includes
    the messages exchanged between the user and the agent. It serves as
    a restricted version of the full State, providing a narrower interface
    to the outside world compared to what is maintained internally.
    """
    input_data: Dict[str,any]
    """Messages track the primary execution state of the agent.

    Typically accumulates a pattern of Human/AI/Human/AI messages; if
    you were to combine this template with a tool-calling ReAct agent pattern,
    it may look like this:

    1. HumanMessage - user input
    2. AIMessage with .tool_calls - agent picking tool(s) to use to collect
         information
    3. ToolMessage(s) - the responses (or errors) from the executed tools
    
        (... repeat steps 2 and 3 as needed ...)
    4. AIMessage without .tool_calls - agent responding in unstructured
        format to the user.

    5. HumanMessage - user responds with the next conversational turn.

        (... repeat steps 2-5 as needed ... )
    
    Merges two lists of messages, updating existing messages by ID.

    By default, this ensures the state is "append-only", unless the
    new message has the same ID as an existing message.

    Returns:
        A new list of messages with the messages from `right` merged into `left`.
        If a message in `right` has the same ID as a message in `left`, the
        message from `right` will replace the message from `left`."""


class Router(TypedDict):
    """Classify user query."""

    logic: str
    type: Literal["more-info", "langchain", "general"]


# This is the primary state of your agent, where you can store any information


@dataclass(kw_only=True)
class AgentState(InputState):
  """
  includes a sections dictionary to store the content generated for each section of the write-up.
  Each node function updates this sections dictionary with its generated content.
  """
  sections: Annotated[dict, merge_dicts] = field(default_factory=dict)
  formatted_document: str = ""  # Add formatted_document attribute
  edited: str = ""  # Add attribute for edited document
  human_messages: list[AnyMessage, add_messages] = field(default_factory=list)