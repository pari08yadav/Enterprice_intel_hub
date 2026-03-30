from .nodes.router import router_node
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.state import GraphState
from src.nodes.retrieval import retrieve_unstructured, retrieve_structured
from src.nodes.llm import generate_response # (Assume defined in llm.py)

def create_graph():
    # 1. Initialize the Memory Saver (Checkpointer)
    # This acts as the "Short-term database" for conversation history
    memory = MemorySaver()
    
    workflow = StateGraph(GraphState)
    
    workflow.add_node("vector_search", retrieve_unstructured)
    workflow.add_node("graph_search", retrieve_structured)
    workflow.add_node("generator", generate_response)

    # ROUTER DICTIONARY (Strings only)
    workflow.add_conditional_edges(
        START,
        router_node,
        {
            "vector": "vector_search",
            "graph": "graph_search",
            "hybrid": "vector_search", # Point to one
            "general": "generator"
        }
    )

    # If it's a hybrid query, we'll manually ensure graph_search 
    # runs after or alongside vector_search.
    workflow.add_edge("vector_search", "graph_search") 
    workflow.add_edge("graph_search", "generator")
    workflow.add_edge("generator", END)

    return workflow.compile(checkpointer=memory)