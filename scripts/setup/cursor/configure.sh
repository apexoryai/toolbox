#!/bin/bash

# scripts/setup/setup_mcp.sh

# This script configures the Model Context Protocol (MCP) for the toolbox.
# It generates the .cursor/mcp.json file with the correct absolute paths
# and environment variables from the .env file.

echo "🚀 Configuring MCP for the toolbox..."

# Ensure the script is run from the project root
cd "$(dirname "$0")/../../.."

# Update .mcp.json with environment variables
python3 scripts/setup/cursor/generate_mcp_json.py

echo "✅ MCP configuration updated successfully!" 