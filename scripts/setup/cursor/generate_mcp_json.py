#!/usr/bin/env python3

import json
import os
from dotenv import load_dotenv

def update_mcp_config():
    """Load .env file and update .cursor/mcp.json with absolute paths and env vars."""
    
    # Get the absolute path of the project's root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Load environment variables from .env file in the project root
    dotenv_path = os.path.join(project_root, '.env')
    load_dotenv(dotenv_path=dotenv_path)
    
    # Path to the mcp.json file
    config_path = os.path.join(project_root, '.cursor', 'mcp.json')
    
    # Define the desired MCP configuration structure
    mcp_config = {
      "mcpServers": {
        "postgres": {
          "command": os.path.join(project_root, 'bin', 'toolbox'),
          "args": [
            "--tools-file",
            os.path.join(project_root, 'config', 'tools.yaml'),
            "--stdio"
          ],
          "env": {
            "POSTGRES_HOST": os.getenv('POSTGRES_HOST', '127.0.0.1'),
            "POSTGRES_PORT": os.getenv('POSTGRES_PORT', '5432'),
            "POSTGRES_DATABASE": os.getenv('POSTGRES_DATABASE', 'toolbox_db'),
            "POSTGRES_USER": os.getenv('POSTGRES_USER', 'toolboxuser'),
            "POSTGRES_PASSWORD": os.getenv('POSTGRES_PASSWORD', 'my-password')
          }
        }
      }
    }
    
    # Create the .cursor directory if it doesn't exist
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Write the updated configuration
    with open(config_path, 'w') as f:
        json.dump(mcp_config, f, indent=2)
    
    print("✅ Generated .cursor/mcp.json with absolute paths and values from .env")

if __name__ == "__main__":
    update_mcp_config() 