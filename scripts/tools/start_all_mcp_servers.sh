#!/bin/bash

# Activate your main venv
source /Users/michaelbevilacqua/Workspace/apexory/toolbox/venv/bin/activate

# Start db_admin server
cd /Users/michaelbevilacqua/Workspace/apexory/toolbox
./bin/toolbox --tools-file config/toolset_db_admin.yaml --address 127.0.0.1 --port 5051 &

# Start hotel_agent server
./bin/toolbox --tools-file config/toolset_hotel_agent.yaml --address 127.0.0.1 --port 5052 &

# Start time server (from its own directory)
cd /Users/michaelbevilacqua/Workspace/servers/src/time
/Users/michaelbevilacqua/Workspace/apexory/toolbox/venv/bin/python -m mcp_server_time &

wait
