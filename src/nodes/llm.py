from openai import OpenAI
import os
from dotenv import load_dotenv
from src.state import GraphState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from utils import logger

load_dotenv()

# March 2026 standard
MODEL = "gemini-3-flash-preview"

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )


# Initialize Gemini 1.5 Flash (Fast and perfect for summarization)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

async def generate_response(state: GraphState):
    print("---GENERATING FINAL RESPONSE---")
    
    # 1. Collect all context gathered from different nodes
    # Because we used operator.add in GraphState, all results are in this list
    context_list = state.get("context", [])
    context_text = "\n".join(context_list) if context_list else "No specific database context provided."
    
    # 2. Get the original user question
    user_query = state["messages"][-1].content
    
    # 3. Build a high-quality System Prompt
    system_prompt = """You are the Enterprise Intelligence Hub for BABAPOTA TRANSPORT.
    Your job is to answer the user's question using the provided context.
    
    RULES:
    - If 'Graph Result' is present, use it for names, roles, and relationships.
    - If 'Vector Result' is present, use it for technical specs, truck counts, or manuals.
    - If no context is provided, answer politely based on general knowledge about the company.
    - Maintain a professional, helpful tone."""

    # 4. Invoke the LLM
    response = await llm.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context: {context_text}\n\nQuestion: {user_query}")
    ])
    
    # Return the AI message to be added to the conversation history
    return {"messages": [response]}