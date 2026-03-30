import asyncio
from src.graph import create_graph
from langchain_core.messages import HumanMessage
from utils import logger

async def main():
    app = create_graph()

    # Define a Thread ID (This is the 'Key' for this specific conversation)
    # In a real app, this would be the User ID or Session ID
    config = {"configurable": {"thread_id": "pari_transport_session_001"}}
    
    print("🚀 Enterprise Intel Hub Active (Type 'exit' to stop)")
    print("-" * 50)

    while True:
        # 3. Interactive Input
        query = input("\n👤 USER: ")
        if query.lower() in ["exit", "quit", "q"]:
            print("👋 Closing connection. Goodbye!")
            break

        inputs = {"messages": [HumanMessage(content=query)]}

        # 4. Stream the Graph Execution
        # Note: We pass 'config' here so the graph knows which thread to load memory from
        async for output in app.astream(inputs, config=config, stream_mode="updates"):
            for node, data in output.items():
                print(f"✔️ Node '{node}' completed.")
                
                # 5. Handle the Final Generator Output
                if node == "generator":
                    last_msg = data["messages"][-1]
                    
                    # Extract content safely (handles both objects and tuples)
                    if hasattr(last_msg, "content"):
                        content = last_msg.content
                    elif isinstance(last_msg, tuple):
                        content = last_msg[1]
                    else:
                        content = str(last_msg)

                    print(f"\n🤖 AGENT: {content}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user.")