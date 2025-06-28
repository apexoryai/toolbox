#!/usr/bin/env python3

import asyncio
from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from toolbox_langchain import ToolboxClient
from src.utils.config import Config

# Load environment variables
load_dotenv()

# Get toolbox URL from configuration
TOOLBOX_URL = Config.get_toolbox_url()

# A single, simple query for the connectivity test
TEST_QUERY = "Search for hotels in Zurich"

# Hotel assistant prompt
HOTEL_PROMPT = """
You're a helpful hotel assistant. You handle hotel searching, booking and
cancellations. Your goal is to use the available tools to answer the user's
request.
"""


async def run_test():
    """Run the agent connectivity test."""
    print("🧪 Running Agent Connectivity Test...")
    print("=" * 50)
    
    # Initialize the model and tools
    try:
        model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        
        # Load the specific toolset for the hotel agent
        client = ToolboxClient(TOOLBOX_URL)
        tools = await client.aload_toolset("hotel-agent")
        
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        
        # Use a unique thread ID for this test session
        config = {"configurable": {"thread_id": "agent-connectivity-test"}}
        
        print(f"✅ Agent initialized with {len(tools)} tools.")
        print(f"▶️  Running test query: '{TEST_QUERY}'")
        
        # Run the pre-defined queries
        inputs = {"messages": [("user", HOTEL_PROMPT + TEST_QUERY)]}
        response = agent.invoke(inputs, config=config)
        
        # Extract and print the response
        last_message = response["messages"][-1].content
        print("\n✅ Test complete. Agent response:")
        print("-" * 40)
        print(last_message)
        print("-" * 40)
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        return
    finally:
        # Clean up
        if 'client' in locals() and hasattr(client, 'aclose'):
            await client.aclose()


if __name__ == "__main__":
    asyncio.run(run_test())