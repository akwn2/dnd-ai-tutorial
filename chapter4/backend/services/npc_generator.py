"""Service for generating NPCs using LangChain."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.models.npc import NPC
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key from the environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is available
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment")

parser = PydanticOutputParser(pydantic_object=NPC)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=google_api_key)

NPC_PROMPT_TEMPLATE = """
You are a creative and experienced TTRPG Game Master. Your task is to generate a detailed Non-Player Character (NPC) based on a user's prompt. The NPC should be interesting and suitable for a fantasy campaign.

The user's prompt is: '{prompt}'

The NPC should have the following attributes:
- A memorable and unique name.
- A defined race (e.g., Human, Elf, Dwarf, Goblin, Orc, Halfling).
- A vocation or profession.
- A distinct personality that's more than a single word.
- A concise backstory.
- Clear motivations that drive their actions.
- A specified role in the story from the list: 'ally', 'enemy', 'quest giver', 'neutral party', 'red herring'.

The output must be a valid JSON object that strictly adheres to the following format. Do not include any other text or formatting in your response. **Output ONLY the JSON object, with no additional commentary, formatting, or code fences. Ensure that any double quotes within the JSON values are properly escaped with a backslash.**

{format_instructions}
"""

npc_prompt = ChatPromptTemplate.from_template(
    template=NPC_PROMPT_TEMPLATE,
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

npc_chain = npc_prompt | llm | parser
