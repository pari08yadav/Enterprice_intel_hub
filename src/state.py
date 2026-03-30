from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator # <--- 1. Import this

class GraphState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    context: Annotated[List[str], operator.add]