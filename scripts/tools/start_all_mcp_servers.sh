#!/bin/bash

# Load environment variables
set -a
[ -f .env ] && source .env
set +a

# Activate your main venv
source /Users/michaelbevilacqua/Workspace/apexory/toolbox/venv/bin/activate

# Start db_admin server in HTTP mode for Python agent
if lsof -i :${DB_ADMIN_PORT} > /dev/null; then
  echo "Port ${DB_ADMIN_PORT} is already in use. Skipping db_admin server startup."
else
  echo "Starting db_admin MCP server in HTTP mode on port ${DB_ADMIN_PORT}..."
  ./bin/toolbox --tools-file config/toolset_db_admin.yaml --address ${MCP_HOST} --port ${DB_ADMIN_PORT} &
fi

# Start hotel_agent server in HTTP mode for Python agent
if lsof -i :${HOTEL_AGENT_PORT} > /dev/null; then
  echo "Port ${HOTEL_AGENT_PORT} is already in use. Skipping hotel_agent server startup."
else
  echo "Starting hotel_agent MCP server in HTTP mode on port ${HOTEL_AGENT_PORT}..."
  ./bin/toolbox --tools-file config/toolset_hotel_agent.yaml --address ${MCP_HOST} --port ${HOTEL_AGENT_PORT} &
fi

# Start textract_agent server in HTTP mode for Python agent
if lsof -i :${TEXTRACT_AGENT_PORT} > /dev/null; then
  echo "Port ${TEXTRACT_AGENT_PORT} is already in use. Skipping textract_agent server startup."
else
  echo "Starting textract_agent MCP server in HTTP mode on port ${TEXTRACT_AGENT_PORT}..."
  ./bin/toolbox --tools-file config/toolset_textract_agent.yaml --address ${MCP_HOST} --port ${TEXTRACT_AGENT_PORT} &
fi

# Start textract FastAPI HTTP server
if lsof -i :${TEXTRACT_HTTP_PORT} > /dev/null; then
  echo "Port ${TEXTRACT_HTTP_PORT} is already in use. Skipping textract FastAPI server startup."
else
  echo "Starting textract FastAPI HTTP server on port ${TEXTRACT_HTTP_PORT}..."
  uvicorn src.agents.textract_http_server:app --host ${MCP_HOST} --port ${TEXTRACT_HTTP_PORT} &
fi

# Start time server (from its own directory)
cd /Users/michaelbevilacqua/Workspace/servers/src/time
/Users/michaelbevilacqua/Workspace/apexory/toolbox/venv/bin/python -m mcp_server_time &

# Confirmation section: check all MCP servers
cd /Users/michaelbevilacqua/Workspace/apexory/toolbox

# Check db_admin (HTTP mode)
if lsof -i :${DB_ADMIN_PORT} > /dev/null; then
  DB_ADMIN_STATUS="HTTP"
else
  DB_ADMIN_STATUS="(not running)"
fi

# Check hotel_agent (HTTP mode)
if lsof -i :${HOTEL_AGENT_PORT} > /dev/null; then
  HOTEL_AGENT_STATUS="HTTP"
else
  HOTEL_AGENT_STATUS="(not running)"
fi

# Check textract_agent (HTTP mode)
if lsof -i :${TEXTRACT_AGENT_PORT} > /dev/null; then
  TEXTRACT_AGENT_STATUS="HTTP"
else
  TEXTRACT_AGENT_STATUS="(not running)"
fi

# Check time_server (assume HTTP, port may vary)
TIME_SERVER_PID=$(ps aux | grep '[m]cp_server_time' | awk '{print $2}')
if [ -n "$TIME_SERVER_PID" ]; then
  TIME_SERVER_STATUS="HTTP"
else
  TIME_SERVER_STATUS="(not running)"
fi

echo ""
echo "========== MCP Server Status =========="
printf "%-15s %-10s %-10s\n" "Server" "Port" "Mode"
printf "%-15s %-10s %-10s\n" "db_admin" "$DB_ADMIN_PORT" "$DB_ADMIN_STATUS"
printf "%-15s %-10s %-10s\n" "hotel_agent" "$HOTEL_AGENT_PORT" "$HOTEL_AGENT_STATUS"
printf "%-15s %-10s %-10s\n" "textract_agent" "$TEXTRACT_AGENT_PORT" "$TEXTRACT_AGENT_STATUS"
printf "%-15s %-10s %-10s\n" "time_server" "(varies)" "$TIME_SERVER_STATUS"
echo ""
echo "Note: db_admin (5051, STDIO) and hotel_agent (5052, STDIO) are managed by Cursor if running."
echo "========================================"

wait
