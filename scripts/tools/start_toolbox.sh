#!/bin/bash

# Source environment variables
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
    echo "Environment variables loaded:"
    echo "  POSTGRES_HOST: ${POSTGRES_HOST}"
    echo "  POSTGRES_PORT: ${POSTGRES_PORT}"
    echo "  POSTGRES_DATABASE: ${POSTGRES_DATABASE}"
    echo "  POSTGRES_USER: ${POSTGRES_USER}"
    echo "  POSTGRES_PASSWORD: [HIDDEN]"
    echo "  TOOLBOX_HOST: ${TOOLBOX_HOST}"
else
    echo "Warning: .env file not found"
fi

# Start the db_admin toolbox server
echo "Starting db_admin toolbox server on port 5051..."
./bin/toolbox --tools-file config/toolset_db_admin.yaml --address "${TOOLBOX_HOST:-127.0.0.1}" --port 5051 &

# Start the hotel_agent toolbox server
echo "Starting hotel_agent toolbox server on port 5052..."
./bin/toolbox --tools-file config/toolset_hotel_agent.yaml --address "${TOOLBOX_HOST:-127.0.0.1}" --port 5052 &

# Start the MCP time server
echo "Starting MCP time server..."
/Users/michaelbevilacqua/Workspace/apexory/toolbox/venv/bin/python -m mcp_server_time --local-timezone America/Denver &

wait 