INTRODUCTION_PROMPT = """ You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the INTRODUCTION section of the report using the following information:
Project Description
Project Description
Brief: {input_data[General Information and data preparation][Project Description][brief]}  # Access 'brief' from the dictionary
Analysis Period: {input_data[General Information and data preparation][general information][Analysis Period]}  # Access 'Analysis Period'

Corn Farm Description
Name: {input_data[General Information and data preparation][Farm description][name]}  # Access 'name'
Location:{input_data[General Information and data preparation][Farm description][location]}  # Access 'location'
Instructions for Writing the INTRODUCTION
Limit to 3–4 short and simple sentences
Use only the provided facts
Do not include opinions or external information
Clearly state that the GHG emission calculation is done according to the requirements of the ISCC EU framework

"""
CALCULATION_METHODOLOGY_PROMPT = """ You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the CALCULATION METHODOLOGY section of the report using the following instructions:
Instructions for Writing the CALCULATION METHODOLOGY
Clearly state that the GHG intensity calculations for corn are conducted according to the methodology outlined in ISCC EU 205 Version 4.1, released in January 2024.
Briefly describe the methodology based on this source.
Use only simple, clear sentences.
Do not introduce any information that is not directly based on the above source.
"""
ALLOCATION_APPROACH_PROMPT = """You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the ALLOCATION APPROACH sub-section of the report using the following instructions:
Instructions for Writing the ALLOCATION APPROACH
Clearly state that 100% of the GHG emissions from farming and transportation are allocated to the main product, corn, as the study assumes no co-products are generated during the farming stage.
Use clear and concise language.
Do not introduce any assumptions or information beyond what is stated above.
 """
SCOPE_OF_ANALYSIS_PROMPT = """ You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the SCOPE OF THE ANALYSIS section of the report using the following instructions:
Instructions for Writing the SCOPE OF THE ANALYSIS
Include the following information
Clearly define the unit in which GHG intensity is expressed:
Define the system boundary, which includes:
All corn farming processes
Transportation of all raw materials used in farming
Transportation of corn to the end user or fuel producer
State the temporal coverage of the analysis:{input_data[General Information and data preparation][general information][Analysis Period]}
State the geographical coverage of the analysis:{input_data[General Information and data preparation][Farm description][location]}
Use clear and concise language
Do not add any information beyond what is provided """
ACTIVITY_DATA_USED_PROMPT = """
You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the ACTIVITY DATA USED section of the report using the following information and instructions:
The input for the task is {input_data}.
You need to go through each key present in the nested input json data(multiple levels). you should proceed till there are no keys present inside that object.
Once you are done processing the data, make a table representing that data.
After making the table make a narrative summary as well, it will summaraize all the contents of the data.

"""

STANDARD_DATA_USED_PROMPT = """ You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the STANDARD DATA section of the report using the following information and instructions:
{input_data} contains the input data in a nested json format. Firstly go through whole input data object, going through each key present in the object till the keys do not have a child key value pair.
Once you are done reviewing it follow the below instructions.
Instructions for Writing the STANDARD DATA USED
Use the data provided above to create tables summarizing various kinds of standard data used for calculating GHG emission of corn of the specified farm
Follow the tables with a brief narrative (1–2 short paragraphs) summarizing and interpreting the key data points or trends.
Keep the language clear, concise, and focused solely on the provided information.
Do not introduce any external data or assumptions.
"""
ASSUMPTIONS_AND_LIMITATIONS_PROMPT = """ You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the LIMITATIONS AND ASSUMPTIONS section of the report using the following information and instructions:
Notes and comments made on the following data points:
Corn products notes:
Moisture content notes:
Gasoline consumption notes:
Diesel CO2 emission factor notes:
Instructions for Writing the LIMITATIONS AND ASSUMPTIONS
Use above notes and comments made for different types of data and write a few assumptions and limitations of the study following the rules and requirements of ISCC EU certification framework and EU RED II regulation.
Keep the language clear, concise, and focused solely on the provided information.
Do not introduce any external data or assumptions.
"""
RESULTS_AND_INTERPRETATION_PROMPT = """ You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the RESULT  section of the report using the following information and instructions:

{input_data} contains the input data in a nested json format. Firstly go through whole input data object, going through each key present in the object till the keys do not have a child key value pair.
Once you are done reviewing it follow the below instructions. Each last key will contain 4 properties CO2, N2O, CH4 and CO2e.

Categorize Acidification and Liming, N2O emissons seperately.

Instructions for Writing the RESULT
Use the data provided above to create a table summarizing the GHG intensity of corn
Make a nice looking chart based on the data summarized in the table
Follow the tables with a brief narrative (1–2 short paragraphs) summarizing and interpreting the key data points or trends.
Keep the language clear, concise, and focused solely on the provided information.
Do not introduce any external data or assumptions.
 """
#RECOMMENDATION_PROMPT = """ write 1 paragraph based on recommendations """
#CONCLUSION_PROMPT = """ conclude the report based on other sections """
REFERENCES_PROMPT= """ You are an expert in greenhouse gas (GHG) emissions accounting for corn (maize) used as a feedstock in the production of biofuels, bioliquids, or biomass fuels for transportation, electricity, heating, or cooling generation. Your work follows the requirements of the International Sustainability & Carbon Certification – European Union (ISCC EU) methodology and the European Union Renewable Energy Directive II (EU RED II) (Directive (EU) 2018/2001).
You have been assigned to prepare a report for a study assessing the GHG intensity of corn under the ISCC EU framework. At this stage, write only the REFERENCE section of the report using the following information and instructions:
Source of the following standard data:
Diesel GHG emission factor:
Gasoline GHG emission factor:
Natural Gas GHG emission factor:


Instructions for Writing the REFERENCE:
Use above notes and comments made for different types of data and write a few REFERENCES of the study following the rules and requirements of ISCC EU certification framework and EU RED II regulation.
Keep the language clear, concise, and focused solely on the provided information.
Do not introduce any external data or assumptions.
 """
ASSEMBLY_PROMPT = """
You are an expert technical writer. Your task is to assemble a comprehensive report on the greenhouse gas (GHG) intensity of corn production based on the provided sections.

Please follow this structure:

Title: Greenhouse Gas Intensity of Corn Production - {input_data[General Information and data preparation][Farm description][name]}

Introduction:
{sections[Introduction]}

Calculation Methodology:
{sections[Calculation Methodology]}

Allocation Approach:
{sections[Allocation Approach]}

Scope of the Analysis:
{sections[Scope of the Analysis]}

Activity Data Used:
{sections[Activity Data Used]}

Standard Data Used:
{sections[Standard Data Used]}

Assumptions and Limitations:
{sections[Assumptions and Limitations]}

Results and Interpretation:
{sections[Results and Interpretation]}

References:
{sections[References]}

Ensure the report is well-structured, coherent, and uses clear and concise language. There might me charts and graph so present them in proper markdown format

"""


HUMAN_EDIT_PROMPT = """
You are an expert technical writer. Your task is to improve a report generated by an AI system.

The current version of the report is shown below. Please review it carefully and make any necessary edits to enhance its clarity, accuracy, and overall quality.

**Original Report:**

{formatted_document}  # This is where the formatted_document from the state is inserted
**Human Message:** {human_message}  # message from human_edit node's state
**Instructions for Editing:**

1.  **General Edits:** If you want to make edits that apply to the entire document, simply make the changes directly in the text provided above.

2.  **Section-Specific Edits:** If you want to edit a particular section of the report (e.g., Introduction, Methodology), please use the following format:
## Section: [Section Name]

[Your edits for the section]
For example, to edit the introduction, you would write:
## Section: Introduction

[Your edits for the introduction section]



Please carefully consider the human's message when making edits. If the message highlights specific issues or suggests improvements, try to incorporate them into your edits.
Now you have to add the changes to the formatted_doc at the specific location i.e. the specified section or sections and then return output as the exact structure of formatted_doc.
Your goal is to produce a high-quality report that is informative, well-structured, and easy to understand.

"""

THINKING_PROMPT = """
I need to incorporate the following changes to the document:
User Request: {human_message}

Current Document State (Version {current_version}):
{current_document}

Edit History:
{edit_history}

Please think through how to implement these changes while maintaining document coherence.
Explain your reasoning process.
"""