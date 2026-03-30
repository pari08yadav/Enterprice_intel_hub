import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore # <--- New Import
from langchain_neo4j import Neo4jGraph
from langchain_core.documents import Document

load_dotenv()

def ingest_data():
    print("🚀 Starting Data Ingestion for Enterprise Intel Hub...")

    # --- DATA DEFINITION ---
    business_docs = [
        "BABAPOTA TRANSPORT specializes in heavy machinery logistics and long-haul transport.",
        "The fleet consists of 10 heavy-duty trucks and 5 flatbed trailers.",
        "Safety is our top priority, with real-time GPS tracking.",
        "The manager handles scheduling, maintenance logs, and client communications."
    ]
    docs = [Document(page_content=text) for text in business_docs]

    # --- PART 1: QDRANT (Vector DB) ---
    print("📦 Indexing to QDRANT using Native Gemini Embeddings...")
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", 
        google_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Use the Qdrant connection from Docker
    vector_db = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"), # http://localhost:6333
        collection_name="enterprise_docs",
        force_recreate=True # Overwrites old data for a clean test
    )
    print("✅ Qdrant Collection 'enterprise_docs' populated.")

    # --- PART 2: NEO4J (Graph DB) ---
    print("🔗 Connecting to Neo4j...")
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"), # bolt://localhost:7687
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        enhanced_schema=False  # <--- ADD THIS LINE TO FIX THE ERROR
    )

    cypher_setup = """
    MERGE (c:Company {name: 'BABAPOTA TRANSPORT'})
    MERGE (p:Person {name: 'Admin', role: 'Manager'})
    MERGE (p)-[:WORKS_AT]->(c)
    MERGE (p)-[:MANAGES]->(c)
    SET c.industry = 'Logistics', c.founded = 2024
    """
    
    graph.query(cypher_setup)
    print("✅ Neo4j Graph relationships established.")
    print("\n🎉 Phase 1 Ingestion Complete!")

if __name__ == "__main__":
    ingest_data()