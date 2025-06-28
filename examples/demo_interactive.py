#!/usr/bin/env python3

"""
Demo script showing how to use the interactive hotel features programmatically.
This script demonstrates both the AI-powered agent and direct tool usage.
"""

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

async def demo_ai_agent():
    """Demo the AI-powered hotel agent."""
    print("🤖 Demo: AI-Powered Hotel Agent")
    print("=" * 40)
    
    try:
        # Initialize the model and tools
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        client = ToolboxClient(TOOLBOX_URL)
        tools = await client.aload_toolset()
        
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        config = {"configurable": {"thread_id": "demo-session"}}
        
        # Demo queries
        demo_queries = [
            "What tables are available in the database?",
            "Find hotels in Basel",
            "Book hotel ID 1",
            "Cancel the booking for hotel ID 1",
            "What hotels are available in Zurich?"
        ]
        
        for query in demo_queries:
            print(f"\n🔍 Query: {query}")
            print("-" * 30)
            
            inputs = {"messages": [("user", query)]}
            response = agent.invoke(inputs, stream_mode="values", config=config)
            
            print(f"🤖 Response: {response['messages'][-1].content}")
        
        await client.aclose()
        
    except Exception as e:
        print(f"❌ Error in AI agent demo: {e}")

async def demo_direct_tools():
    """Demo direct tool usage without AI."""
    print("\n🔧 Demo: Direct Tool Usage")
    print("=" * 40)
    
    try:
        client = ToolboxClient(TOOLBOX_URL)
        tools = await client.aload_toolset()
        
        # Create tool mapping
        tool_map = {tool.name: tool for tool in tools}
        
        # Demo tool invocations
        demos = [
            ("list_tables", {}),
            ("search-hotels-by-name", {"name": "Hilton"}),
            ("search-hotels-by-location", {"location": "Basel"}),
            ("book-hotel", {"hotel_id": 1}),
            ("cancel-booking", {"hotel_id": 1})
        ]
        
        for tool_name, params in demos:
            if tool_name in tool_map:
                tool = tool_map[tool_name]
                print(f"\n🔧 Tool: {tool_name}")
                print(f"📝 Description: {tool.description}")
                print(f"📋 Parameters: {params}")
                
                result = await tool.ainvoke(params)
                print(f"✅ Result: {result}")
            else:
                print(f"❌ Tool {tool_name} not found")
        
        await client.aclose()
        
    except Exception as e:
        print(f"❌ Error in direct tools demo: {e}")

async def demo_interactive_features():
    """Demo the interactive features."""
    print("\n🎮 Demo: Interactive Features")
    print("=" * 40)
    print("This demo shows how to use the interactive features:")
    print()
    print("1. AI-Powered Interactive Agent:")
    print("   python interactive_hotel_agent.py")
    print("   - Ask natural language questions")
    print("   - Get AI-powered responses")
    print("   - Full conversation capabilities")
    print()
    print("2. Direct Tool Tester:")
    print("   python examples/interactive_tool_test.py")
    print("   - Test individual tools")
    print("   - No AI model required")
    print("   - Faster for debugging")
    print()
    print("3. Programmatic Usage:")
    print("   - Use ToolboxClient directly")
    print("   - Integrate with your own applications")
    print("   - Custom AI agents")

async def main():
    """Run all demos."""
    print("🏨 Hotel Management System - Interactive Features Demo")
    print("=" * 60)
    
    # Check if toolbox server is running
    try:
        client = ToolboxClient(TOOLBOX_URL)
        await client.aload_toolset()
        await client.aclose()
        print("✅ Toolbox server is running")
    except Exception as e:
        print(f"❌ Toolbox server not accessible: {e}")
        print("Please start the toolbox server first:")
        print("./scripts/start_toolbox.sh")
        return
    
    # Run demos
    await demo_ai_agent()
    await demo_direct_tools()
    await demo_interactive_features()
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("Try the interactive features:")
    print("  python interactive_hotel_agent.py")
    print("  python examples/interactive_tool_test.py")

if __name__ == "__main__":
    asyncio.run(main()) 