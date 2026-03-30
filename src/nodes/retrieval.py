# from src.database import retriever, graph, client
# from utils import logger

# async def retrieve_unstructured(state):
#     query = state["messages"][-1].content
#     docs = await retriever.ainvoke(query)
#     return {"context": [d.page_content for d in docs]}

# async def retrieve_structured(state):
#     query = state["messages"][-1].content
    
#     logger.info(query)
#     cypher_prompt = f"Convert to Cypher for schema {graph.schema}: {query}"
    
#     response = client.chat.completions.create(
#         model="gemini-2.5-flash",
#         messages=[{"role": "user", "content": cypher_prompt}]
#     )
#     cypher_query = response.choices[0].message.content
    
#     try:
#         results = graph.query(cypher_query)
#         return {"context": [f"Graph Result: {str(results)}"]}
#     except:
#         return {"context": ["No graph data found."]}




from src.database import retriever, graph, client
from utils import logger
import re

async def retrieve_unstructured(state):
    print("---RETRIEVING FROM VECTOR DB---")
    query = state["messages"][-1].content
    
    try:
        # Await the vector store response
        docs = await retriever.ainvoke(query)
        context = [d.page_content for d in docs]
        
        if not context:
            return {"context": ["System Note: No relevant technical documents found in Vector DB."]}
            
        return {"context": context}
    
    except Exception as e:
        logger.error(f"Vector Search Failure: {e}")
        # Return a note so the LLM knows the DB is unreachable
        return {"context": ["System Note: Vector database (Qdrant) is currently unavailable."]}

async def retrieve_structured(state):
    print("---RETRIEVING FROM GRAPH DB---")
    query = state["messages"][-1].content
    
    # 1. Manually define the schema (Much safer and faster)
    # This prevents the 'graph.schema' syntax error
    manual_schema = """
    Nodes: 
    - Person {name: STRING, role: STRING}
    - Company {name: STRING}
    Relationships:
    - (Person)-[:WORKS_AT]->(Company)
    - (Person)-[:MANAGES]->(Company)
    """
    
    cypher_prompt = f"""
    Task: Convert the user question into a Neo4j Cypher query.
    Schema: {manual_schema}
    Question: {query}
    
    Instructions:
    - Return ONLY the query string. No markdown, no backticks.
    - Use case-insensitive matches for names.
    - To find a manager, look for Person where role = 'Manager'.
    - Example: MATCH (p:Person {{role: 'Manager'}}) RETURN p.name AS name, p.role AS role
    """
    
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash", 
            messages=[{"role": "user", "content": cypher_prompt}]
        )
        cypher_query = response.choices[0].message.content.strip()
        
        # Clean markdown
        cypher_query = re.sub(r'```[a-zA-Z]*\n?', '', cypher_query).replace('```', '').strip()
        
        print(f"DEBUG: Executing Cypher -> {cypher_query}")

        # 2. Execute
        results = graph.query(cypher_query)
        
        if not results:
            return {"context": ["Graph Result: No matching personnel found."]}
            
        return {"context": [f"Graph Result: {str(results)}"]}
        
    except Exception as e:
        print(f"❌ NEO4J ERROR: {e}") 
        return {"context": ["System Note: Graph database query failed."]}