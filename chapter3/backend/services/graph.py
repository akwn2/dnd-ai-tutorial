"""LangGraph setup for the TTRPG GM Assistant."""
import re
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from backend.models.chat import AgentState
from backend.services.npc_generator import npc_chain
from backend.services.dice_roller import roll_dice

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

class RouteQuery(BaseModel):
    """Route a user query to the most relevant tool."""
    tool_name: str = Field(
        ...,
        description="The name of the tool to use.",
        enum=["npc_generator", "dice_roller", "general_response"],
    )

# Create the router
router = llm.with_structured_output(RouteQuery)

def generate_npc_node(state: AgentState):
    """Generates an NPC based on the user's prompt."""
    prompt = state["messages"][-1].content
    try:
        npc_data = npc_chain.invoke({"prompt": prompt})
        formatted_npc = f"""
**Name:** {npc_data.name}
**Race:** {npc_data.race}
**Vocation:** {npc_data.vocation}
**Personality:** {npc_data.personality}
**Backstory:** {npc_data.backstory}
**Motivations:** {npc_data.motivations}
**Role in Story:** {npc_data.role_in_story.title()}
"""
        return {"messages": [AIMessage(content=formatted_npc)]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"An error occurred while generating the NPC: {e}")]}

def supervisor_node(state: AgentState):
    """Determines which node to route to based on the user's prompt."""
    prompt = state["messages"][-1].content
    route = router.invoke([HumanMessage(content=prompt)])
    return {"next_node": route.tool_name}

def dice_roller_node(state: AgentState):
    """Rolls dice based on the user's prompt."""
    prompt = state["messages"][-1].content
    dice_string_match = re.search(r'\d+d\d+', prompt.lower())
    if dice_string_match:
        dice_string = dice_string_match.group(0)
        result = roll_dice.invoke(dice_string)
        return {"messages": [AIMessage(content=result)]}
    return {"messages": [AIMessage(content="I couldn't find a valid dice notation. Please use 'XdY'.")]}

def general_response_node(state: AgentState):
    """Generates a general response if the prompt doesn't match any other nodes."""
    prompt = state["messages"][-1].content
    # Use a new LLM instance for the general response
    general_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    response = general_llm.invoke(state["messages"])
    return {"messages": [AIMessage(content=f"I don't have the skill to answer that question yet, but without that extra information, I would answer it like this:\n\n{response.content}")]}

builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor_node)
builder.add_node("npc_generator", generate_npc_node)
builder.add_node("dice_roller", dice_roller_node)
builder.add_node("general_response", general_response_node)
builder.set_entry_point("supervisor")
builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next_node"],
    {
        "npc_generator": "npc_generator",
        "dice_roller": "dice_roller",
        "general_response": "general_response",
    },
)
builder.add_edge("npc_generator", END)
builder.add_edge("dice_roller", END)
builder.add_edge("general_response", END)
graph = builder.compile()
