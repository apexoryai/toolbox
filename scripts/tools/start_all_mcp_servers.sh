#!/bin/bash

# Activate your main venv
source /Users/michaelbevilacqua/Workspace/apexory/toolbox/venv/bin/activate

# Start db_admin server in HTTP mode for Python agent (always on 5054)
if lsof -i :5054 > /dev/null; then
  echo "Port 5054 is already in use. Skipping db_admin server startup."
else
  echo "Starting db_admin MCP server in HTTP mode on port 5054..."
  ./bin/toolbox --tools-file config/toolset_db_admin.yaml --address 127.0.0.1 --port 5054 &
fi

# Start hotel_agent server in HTTP mode for Python agent (always on 5053)
if lsof -i :5053 > /dev/null; then
  echo "Port 5053 is already in use. Skipping hotel_agent server startup."
else
  echo "Starting hotel_agent MCP server in HTTP mode on port 5053..."
  ./bin/toolbox --tools-file config/toolset_hotel_agent.yaml --address 127.0.0.1 --port 5053 &
fi

# Start time server (from its own directory)
cd /Users/michaelbevilacqua/Workspace/servers/src/time
/Users/michaelbevilacqua/Workspace/apexory/toolbox/venv/bin/python -m mcp_server_time &

# Confirmation section: check all three MCP servers
cd /Users/michaelbevilacqua/Workspace/apexory/toolbox

# Check db_admin (HTTP mode)
if lsof -i :5054 > /dev/null; then
  DB_ADMIN_STATUS="HTTP"
else
  DB_ADMIN_STATUS="(not running)"
fi

# Check hotel_agent (HTTP mode)
if lsof -i :5053 > /dev/null; then
  HOTEL_AGENT_STATUS="HTTP"
else
  HOTEL_AGENT_STATUS="(not running)"
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
printf "%-15s %-10s %-10s\n" "db_admin" "5054" "$DB_ADMIN_STATUS"
printf "%-15s %-10s %-10s\n" "hotel_agent" "5053" "$HOTEL_AGENT_STATUS"
printf "%-15s %-10s %-10s\n" "time_server" "(varies)" "$TIME_SERVER_STATUS"
echo ""
echo "Note: db_admin (5051, STDIO) and hotel_agent (5052, STDIO) are managed by Cursor if running."
echo "========================================"

wait
