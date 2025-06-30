#!/bin/bash

# List of known MCP server ports and their expected modes
SERVERS=(
  "db_admin:5051:STDIO"
  "db_admin:5054:HTTP"
  "hotel_agent:5052:STDIO"
  "hotel_agent:5053:HTTP"
)

printf "%-15s %-10s %-10s %-10s\n" "Server" "Port" "Mode" "PID"

for entry in "${SERVERS[@]}"; do
  IFS=":" read -r name port mode <<< "$entry"
  pid=$(lsof -ti :$port)
  if [ -n "$pid" ]; then
    printf "%-15s %-10s %-10s %-10s\n" "$name" "$port" "$mode" "$pid"
  else
    printf "%-15s %-10s %-10s %-10s\n" "$name" "$port" "$mode" "(not running)"
  fi
done

# Check time_server (by process name)
TIME_SERVER_PID=$(ps aux | grep '[m]cp_server_time' | awk '{print $2}')
if [ -n "$TIME_SERVER_PID" ]; then
  echo "time_server      (varies)   HTTP       $TIME_SERVER_PID"
else
  echo "time_server      (varies)   HTTP       (not running)"
fi 