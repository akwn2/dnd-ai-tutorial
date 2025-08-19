"""Service for generating encounters using LangChain."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.models.encounter import Encounter

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
encounter_parser = PydanticOutputParser(pydantic_object=Encounter)
encounter_prompt_template = """
You are a creative and experienced TTRPG Game Master. Your task is to generate a detailed combat encounter based on a user's prompt. The encounter should be interesting, challenging, and suitable for a fantasy campaign.

The user's prompt is: '{prompt}'

The encounter should have the following attributes:
- A title for the encounter.
- A short, evocative description of the scene.
- A list of monsters involved, including their names, challenge ratings (e.g., "CR 1/2"), and a brief description.
- Recommended tactics for the monsters to use.
- A description of the terrain where the encounter takes place.

The output must be a valid JSON object that strictly adheres to the following format. Do not include any other text or formatting in your response.

{format_instructions}
"""
encounter_prompt = ChatPromptTemplate.from_template(
    template=encounter_prompt_template,
    partial_variables={"format_instructions": encounter_parser.get_format_instructions()},
)
encounter_chain = encounter_prompt | llm | encounter_parser
