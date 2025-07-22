"""Define the configurable parameters for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated

from src.retrieval_graph import prompts
from src.shared.configuration import BaseConfiguration


@dataclass(kw_only=True)
class AgentConfiguration(BaseConfiguration):
    """The configuration for the agent."""

    # models

    query_model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="openai/gpt-4o",
        metadata={
            "description": "The language model used for processing and refining queries. Should be in the form: provider/model-name."
        },
    )

    response_model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="openai/gpt-4o",
        metadata={
            "description": "The language model used for generating responses. Should be in the form: provider/model-name."
        },
    )

    # prompts

    # router_system_prompt: str = field(
    #     default=prompts.ROUTER_SYSTEM_PROMPT,
    #     metadata={
    #         "description": "The system prompt used for classifying user questions to route them to the correct node."
    #     },
    # )

    # more_info_system_prompt: str = field(
    #     default=prompts.MORE_INFO_SYSTEM_PROMPT,
    #     metadata={
    #         "description": "The system prompt used for asking for more information from the user."
    #     },
    # )

    # general_system_prompt: str = field(
    #     default=prompts.GENERAL_SYSTEM_PROMPT,
    #     metadata={
    #         "description": "The system prompt used for responding to general questions."
    #     },
    # )

    # research_plan_system_prompt: str = field(
    #     default=prompts.RESEARCH_PLAN_SYSTEM_PROMPT,
    #     metadata={
    #         "description": "The system prompt used for generating a research plan based on the user's question."
    #     },
    # )

    # generate_queries_system_prompt: str = field(
    #     default=prompts.GENERATE_QUERIES_SYSTEM_PROMPT,
    #     metadata={
    #         "description": "The system prompt used by the researcher to generate queries based on a step in the research plan."
    #     },
    # )

    # response_system_prompt: str = field(
    #     default=prompts.RESPONSE_SYSTEM_PROMPT,
    #     metadata={"description": "The system prompt used for generating responses."},
    # )

      # prompts
    introduction_prompt:str = field(
      default=prompts.INTRODUCTION_PROMPT,
      metadata={
          "description":"The introduction prompt for the report agent."
      }
  )
    calculation_methodology_prompt: str = field(
      default=prompts.CALCULATION_METHODOLOGY_PROMPT,
      metadata={
          "description":"The methodology prompt for the report agent."
      }
  )

    allocation_approach_prompt: str = field(
      default=prompts.ALLOCATION_APPROACH_PROMPT,
      metadata={
          "description":"The allocation approach prompt for the report agent."
      }
  )

    scope_of_analysis_prompt: str = field(
      default=prompts.SCOPE_OF_ANALYSIS_PROMPT,
      metadata={
          "description":"The scope of analysis prompt for the report agent."
      }
  )

    activity_data_used_prompt: str = field(
      default=prompts.ACTIVITY_DATA_USED_PROMPT,
      metadata={
          "description":"The data used prompt for the report agent."
      }
  )

    standard_data_used_prompt: str = field(
      default=prompts.STANDARD_DATA_USED_PROMPT,
      metadata={
          "description":"The data used prompt for the report agent."
      }
  )

    assumptions_and_limitations_prompt: str = field(
      default=prompts.ASSUMPTIONS_AND_LIMITATIONS_PROMPT,
      metadata={
          "description":"The assumptions and limitations prompt for the report agent."
      }
  )

    results_and_interpretation_prompt: str = field(
      default=prompts.RESULTS_AND_INTERPRETATION_PROMPT,
      metadata={
          "description":"The results and interpretation prompt for the report agent."
      }
  )

  # conclusion_prompt: str = field(
  #     default=CONCLUSION_PROMPT,
  #     metadata={
  #         "description":"The conclusion prompt for the report agent."
  #     }
  # )

    references_prompt: str = field(
      default=prompts.REFERENCES_PROMPT,
      metadata={
          "description":"The references prompt for the report agent."
      }
  )

    assembly_prompt: str = field(
      default=prompts.ASSEMBLY_PROMPT,
      metadata={
          "description":"The assembling prompt for the report agent."
      }
  )

    human_edit_prompt: str = field(
      default=prompts.HUMAN_EDIT_PROMPT,
      metadata={
          "description":"The human edit prompt for the report agent."
      }
  )