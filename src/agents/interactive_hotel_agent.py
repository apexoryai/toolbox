#!/usr/bin/env python3

import asyncio
from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from toolbox_langchain import ToolboxClient
from src.utils.config import Config

# Load environment variables from .env file
load_dotenv()

# Get toolbox URL from configuration
TOOLBOX_URL = Config.get_toolbox_url()

# Hotel assistant prompt
HOTEL_PROMPT = """
You're a helpful hotel assistant. You handle hotel searching, booking and
cancellations. When the user searches for a hotel, mention it's name, id,
location and price tier. Always mention hotel ids while performing any
searches. This is very important for any operations. For any bookings or
cancellations, please provide the appropriate confirmation. Be sure to
update checkin or checkout dates if mentioned by the user.
Don't ask for confirmations from the user.

If you cannot fulfill a user's request using the available tools,
politely inform them that you cannot help.
"""

async def interactive_hotel_agent():
    """Interactive hotel agent that accepts user queries."""
    
    print("🏨 Welcome to the Interactive Hotel Assistant!")
    print("=" * 50)
    print("You can ask me to:")
    print("- Search for hotels by name or location")
    print("- Book hotels")
    print("- Cancel bookings")
    print("- Get hotel information")
    print("- Ask general questions about hotels")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the session")
    print("Type 'help' to see this message again")
    print("=" * 50)
    
    # Initialize the model and tools
    try:
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        
        # Load the tools from the Toolbox server
        client = ToolboxClient(TOOLBOX_URL)
        tools = await client.aload_toolset("hotel-agent")
        
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        
        # Use a unique thread ID for this session
        config = {"configurable": {"thread_id": "interactive-session"}}
        
        print("✅ Connected to hotel database and AI model!")
        print()
        
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        print("Make sure:")
        print("1. The toolbox server is running: ./scripts/start_toolbox.sh")
        print("2. Your GOOGLE_API_KEY is set in .env file")
        return
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_query = input("\n🤔 What would you like to know about hotels? ").strip()
            
            # Check for exit commands
            if user_query.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thank you for using the Hotel Assistant! Goodbye!")
                break
            
            # Check for help command
            if user_query.lower() == 'help':
                print("\n🏨 Hotel Assistant Help:")
                print("=" * 30)
                print("You can ask me to:")
                print("- Search for hotels by name or location")
                print("- Book hotels")
                print("- Cancel bookings")
                print("- Get hotel information")
                print("- Ask general questions about hotels")
                print("=" * 30)
                continue
            
            # Skip empty queries
            if not user_query:
                continue
            
            print("\n🤖 Processing your request...")
            
            # Process the query with the agent
            inputs = {"messages": [("user", HOTEL_PROMPT + user_query)]}
            try:
                # Use a standard, non-streaming invoke for robustness
                response = agent.invoke(inputs, config=config)
                
                print("\n💬 Assistant:")
                if response and "messages" in response:
                    last_message = response["messages"][-1]
                    if hasattr(last_message, 'content'):
                        print(last_message.content)
                    else:
                        # This case handles unexpected but valid-looking response structures
                        print("I'm sorry, I received a response I couldn't understand. Please try again.")
                else:
                    # This case handles empty or invalid responses
                    print("I'm not sure how to respond to that. Could you please try asking in a different way?")

            except Exception:
                # A generic error for the user is better than a technical one.
                # This catches the "thought" parsing error and others.
                print("\n❌ I'm sorry, I ran into a problem processing that request.")
                print("   Please try rephrasing your question or type 'help'.")

        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
    
    # Clean up
    try:
        if hasattr(client, 'aclose'):
            await client.aclose()
        elif hasattr(client, 'close'):
            await client.close()
    except:
        pass

if __name__ == "__main__":
    print("🚀 Starting Interactive Hotel Agent...")
    asyncio.run(interactive_hotel_agent()) 