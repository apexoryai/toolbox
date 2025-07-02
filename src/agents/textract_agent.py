from toolbox_langchain import ToolboxClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import sys
import json
from dotenv import load_dotenv
from src.utils.config import Config

# Load environment variables from .env file
load_dotenv()

TOOLBOX_URL = Config.get_toolbox_url()

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/agents/textract_agent.py /path/to/your/file.pdf")
        return

    file_path = sys.argv[1]
    client = ToolboxClient(TOOLBOX_URL)  # Use hotel agent MCP server

    tools = client.load_toolset("hotel-agent")
    extract_tool = None
    for tool in tools:
        if getattr(tool, "name", None) == "extract-text":
            extract_tool = tool
            break

    if extract_tool is None:
        print("extract-text tool not found in hotel-agent toolset.")
        return

    # Use .invoke() to avoid deprecation warning
    result = extract_tool.invoke(json.dumps({"file_path": file_path}))
    print("Result from hotel agent extract-text tool:")
    print(result)

if __name__ == "__main__":
    main() 