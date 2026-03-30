from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()

# Define the "Mental Model" for the Router
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["vector", "graph", "hybrid", "general"] = Field(
        description="Given a user query, decide if it needs Vector data, Graph data, both, or neither."
    )

# Initialize the Router LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
structured_router = llm.with_structured_output(RouteQuery)

async def router_node(state):
    print("---ROUTING QUERY---")
    
    # 3. Define the Expert Routing Instructions
    system_prompt = SystemMessage(content="""You are an expert router for BABAPOTA TRANSPORT.
    Your job is to look at the user query and determine which data source is required:
    
    - 'graph': Use this for questions about PEOPLE, ROLES, NAMES, MANAGERS, or organizational structure.
    - 'vector': Use this for technical SPECS, TRUCK types, counts, maintenance, or manuals.
    - 'hybrid': Use this ONLY if the user asks about BOTH people and technical truck details in one sentence.
    - 'general': Use this for greetings (Hi, Hello) or generic talk that doesn't need a database.
    
    Strictly follow these rules to ensure the correct database is triggered.""")

    query = state["messages"][-1].content
    user_input = HumanMessage(content=query)
    
    # 4. Invoke with System Instructions
    result = await structured_router.ainvoke([system_prompt, user_input])
    
    print(f"DEBUG: Router decided on -> {result.datasource}")
    
    return result.datasource