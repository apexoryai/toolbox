#!/usr/bin/env python3

"""
Interactive tool testing script for the hotel management toolbox.
This script allows you to test individual tools without requiring an AI model.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from toolbox_langchain import ToolboxClient
from src.utils.config import Config

# Load environment variables
load_dotenv()

# Get toolbox URL from configuration
TOOLBOX_URL = Config.get_toolbox_url()

async def interactive_tool_test():
    """Interactive tool tester for hotel tools."""
    
    print("🔧 Interactive Hotel Tool Tester")
    print("=" * 40)
    print("This tool allows you to test hotel tools directly.")
    print("It will connect to the toolbox server and show a list of available tools.")
    print("=" * 40)
    print("Type 'quit' or 'exit' to end")
    print("Type 'help' to see this message again")
    print("=" * 40)
    
    # Initialize the client
    try:
        client = ToolboxClient(TOOLBOX_URL)
        tools = await client.aload_toolset()
        
        # Create a mapping of tool names to tools
        tool_map = {tool.name: tool for tool in tools}
        
        print("✅ Connected to toolbox server!")
        print(f"📦 Loaded {len(tools)} tools")
        print()
        
    except Exception as e:
        print(f"❌ Error connecting to toolbox: {e}")
        print("Make sure the toolbox server is running: ./scripts/start_toolbox.sh")
        return
    
    # Interactive loop
    while True:
        try:
            print("\nAvailable tools:")
            for i, tool_name in enumerate(tool_map.keys(), 1):
                tool = tool_map[tool_name]
                print(f"{i}. {tool_name} - {tool.description}")
            
            print("\n" + "=" * 40)
            user_input = input("Enter tool name or number (or 'quit'): ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            # Check for help command
            if user_input.lower() == 'help':
                print("\n🔧 Tool Tester Help:")
                print("=" * 25)
                print("You can:")
                print("- Enter tool name (e.g., 'search-hotels-by-name')")
                print("- Enter tool number (e.g., '1')")
                print("- Type 'quit' to exit")
                print("=" * 25)
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Find the tool
            selected_tool = None
            
            # Try to match by number
            try:
                tool_index = int(user_input) - 1
                if 0 <= tool_index < len(tools):
                    selected_tool = tools[tool_index]
            except ValueError:
                # Try to match by name
                if user_input in tool_map:
                    selected_tool = tool_map[user_input]
            
            if not selected_tool:
                print(f"❌ Tool '{user_input}' not found. Please try again.")
                continue
            
            print(f"\n🔧 Testing tool: {selected_tool.name}")
            print(f"📝 Description: {selected_tool.description}")
            
            # Get parameters for the tool
            if hasattr(selected_tool, 'args_schema'):
                schema = selected_tool.args_schema.model_json_schema()
                properties = schema.get('properties', {})
                
                if properties:
                    print(f"📋 Parameters needed:")
                    params = {}
                    
                    for param_name, param_info in properties.items():
                        param_type = param_info.get('type', 'string')
                        param_desc = param_info.get('description', 'No description')
                        print(f"   - {param_name} ({param_type}): {param_desc}")
                        
                        # Get parameter value from user
                        param_value = input(f"Enter {param_name}: ").strip()
                        
                        # Convert to appropriate type
                        if param_type == 'integer':
                            try:
                                param_value = int(param_value)
                            except ValueError:
                                print(f"❌ Invalid integer for {param_name}")
                                continue
                        
                        params[param_name] = param_value
                    
                    # Execute the tool
                    print(f"\n🚀 Executing {selected_tool.name} with parameters: {params}")
                    result = await selected_tool.ainvoke(params)
                    print(f"✅ Result: {result}")
                else:
                    print("ℹ️ No parameters needed for this tool")
                    result = await selected_tool.ainvoke({})
                    print(f"✅ Result: {result}")
            else:
                print("ℹ️ No parameter schema available")
                result = await selected_tool.ainvoke({})
                print(f"✅ Result: {result}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")
    
    # Clean up
    try:
        if hasattr(client, 'aclose'):
            await client.aclose()
        elif hasattr(client, 'close'):
            await client.close()
    except:
        pass

if __name__ == "__main__":
    print("🚀 Starting Interactive Tool Tester...")
    asyncio.run(interactive_tool_test()) 