# Enterprise Intel Hub: Agentic Hybrid RAG for Transport Logistics

A high-performance AI Agent built with LangGraph, Gemini 2.5 Flash, Neo4j (Graph DB), and Qdrant (Vector DB). This system is designed to handle complex logistics queries by intelligently routing between structured organizational data and unstructured technical documentation.

---

## The Architecture: "Thinking Before Acting"

Unlike standard RAG pipelines that hit a database blindly, this agent uses a Router-Provider pattern:

1. Intent Classification: A Pydantic-powered Router identifies if a query needs Graph data (People/Roles), Vector data (Truck Specs), or a Hybrid of both.
2. Parallel Execution: Hybrid queries trigger both Neo4j and Qdrant concurrently using LangGraph's state-branching, reducing latency.
3. Stateful Memory: Integrated `MemorySaver` allows the agent to handle multi-turn conversations (e.g., "Who is the manager?" -> "What is his role?").
4. Resilient Retrieval: Custom error-handling wrappers ensure the agent "fails gracefully" if a database is unreachable.

---

## 🛠️ Tech Stack

* Orchestration: LangGraph (Stateful Multi-Agent Framework)
* LLM: Google Gemini 1.5 Flash
* Graph Database: Neo4j (Cypher Query Language)
* Vector Database: Qdrant (Semantic Search)
* Schema Enforcement: Pydantic

---

## Key Challenges & Solutions

### 1. The Neo4j/LangChain Schema Bug

Challenge: The standard `graph.schema` call in LangChain triggered an `IS OF TYPE` syntax error in Neo4j Community Edition.
Solution: Implemented a Manual Schema Mapping strategy. By hardcoding the schema in the prompt, I bypassed the library bug, reduced database latency by ~200ms, and improved Cypher generation accuracy.

### 2. Parallel State Merging

Challenge: Merging context from two different databases running in parallel without overwriting data.
Solution: Leveraged `Annotated[List, operator.add]` in the LangGraph `GraphState`. This ensures that context from both Vector and Graph nodes is appended seamlessly before reaching the Generator.

---

## Installation & Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/pari08yadav/Enterprice_intel_hub.git
   cd enterprise_intel_hub
   ```

2. docker compose up   # for starting the docker.

3. python main.py      # for running the project 
