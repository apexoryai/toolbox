quit
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

# DB Admin assistant prompt
ADMIN_PROMPT = """
You are a database administrator assistant. You can list tables, describe table schemas, and perform other admin tasks. Only use the available tools. Do not attempt to answer questions outside of database administration.
"""

async def db_admin_agent():
    """Interactive DB admin agent that accepts user queries."""
    print("\U0001F4BE Welcome to the DB Admin Assistant!")
    print("=" * 50)
    print("You can ask me to:")
    print("- List tables in the database")
    print("- Describe table schemas")
    print("- Perform other admin tasks defined in the db-admin toolset")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the session")
    print("Type 'help' to see this message again")
    print("=" * 50)

    try:
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        client = ToolboxClient(TOOLBOX_URL)
        tools = await client.aload_toolset("db-admin")
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        config = {"configurable": {"thread_id": "db-admin-session"}}
        print("✅ Connected to toolbox server and AI model!\n")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        print("Make sure:")
        print("1. The toolbox server is running: ./scripts/tools/start_toolbox.sh")
        print("2. Your GOOGLE_API_KEY is set in .env file")
        return

    while True:
        try:
            user_query = input("\n🛠️ DB Admin> ").strip()
            if user_query.lower() in ["quit", "exit", "bye"]:
                print("👋 Thank you for using the DB Admin Assistant! Goodbye!")
                break
            if user_query.lower() == "help":
                print("\n\U0001F4BE DB Admin Assistant Help:")
                print("=" * 30)
                print("You can ask me to:")
                print("- List tables in the database")
                print("- Describe table schemas")
                print("- Perform other admin tasks defined in the db-admin toolset")
                print("=" * 30)
                continue
            if not user_query:
                continue
            print("\n🤖 Processing your request...")
            inputs = {"messages": [("user", ADMIN_PROMPT + user_query)]}
            try:
                response = agent.invoke(inputs, config=config)
                print("\n💬 Assistant:")
                if response and "messages" in response:
                    last_message = response["messages"][-1]
                    if hasattr(last_message, 'content'):
                        print(last_message.content)
                    else:
                        print("I'm sorry, I received a response I couldn't understand. Please try again.")
                else:
                    print("I'm not sure how to respond to that. Could you please try asking in a different way?")
            except Exception:
                print("\n❌ I'm sorry, I ran into a problem processing that request.")
                print("   Please try rephrasing your question or type 'help'.")
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
    try:
        if hasattr(client, 'aclose'):
            await client.aclose()
        elif hasattr(client, 'close'):
            await client.close()
    except:
        pass

if __name__ == "__main__":
    print("🚀 Starting DB Admin Agent...")
    asyncio.run(db_admin_agent()) 