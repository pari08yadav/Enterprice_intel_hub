# from dotenv import load_dotenv
# import os
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain_community.graphs import Neo4jGraph
# from openai import OpenAI


# load_dotenv()

# # Gemini via OpenAI Client
# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

# )

# # Vector DB
# embeddings = OpenAIEmbeddings()
# vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
# retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# # Graph DB
# graph = Neo4jGraph(
#     url=os.getenv("NEO4J_URI"), 
#     username=os.getenv("NEO4J_USERNAME"), 
#     password=os.getenv("NEO4J_PASSWORD")
# )



import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_neo4j import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import OpenAI

load_dotenv()

# 1. Native Gemini Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. Qdrant (The Docker Vector DB)
# We use from_existing_collection because we already ran ingest.py
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="enterprise_docs",
    url=os.getenv("QDRANT_URL") # http://localhost:6333
)
retriever = vector_db.as_retriever()

# 3. Neo4j (The Docker Graph DB)
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
    enhanced_schema=False
)

# # Gemini via OpenAI Client
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)