#!/usr/bin/env python3
"""
Test script for MCP time server integration.
Demonstrates how the MCP time server provides time tools to the toolbox.
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path


def test_mcp_time_server_direct():
    """Test the MCP time server directly."""
    print("🕐 Testing MCP Time Server Directly\n")
    
    try:
        # Test the MCP time server with correct timezone
        result = subprocess.run([
            "python", "-m", "mcp_server_time", "--local-timezone", "America/Denver"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ MCP time server started successfully")
        else:
            print(f"❌ MCP time server failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("✅ MCP time server is running (timeout expected for stdio server)")
    except Exception as e:
        print(f"❌ Error testing MCP time server: {e}")


def test_timezone_resolution():
    """Test timezone resolution with the MCP time server."""
    print("\n🌍 Testing Timezone Resolution\n")
    
    # Test with the correct IANA timezone identifier
    try:
        result = subprocess.run([
            "python", "-c", 
            "from zoneinfo import ZoneInfo; print('America/Denver:', ZoneInfo('America/Denver'))"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Timezone 'America/Denver' is valid")
            print(f"   {result.stdout.strip()}")
        else:
            print(f"❌ Timezone test failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error testing timezone: {e}")


def test_cursor_mcp_config():
    """Test that the Cursor MCP configuration is correct."""
    print("\n⚙️ Testing Cursor MCP Configuration\n")
    
    config_path = Path(".cursor/mcp.json")
    if not config_path.exists():
        print("❌ .cursor/mcp.json not found")
        return
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check if time_server is configured
        if "time_server" in config.get("mcpServers", {}):
            time_config = config["mcpServers"]["time_server"]
            print("✅ MCP time server is configured in Cursor")
            print(f"   Command: {time_config.get('command')}")
            print(f"   Args: {time_config.get('args')}")
        else:
            print("❌ MCP time server not found in configuration")
        
        # Check if toolset files are correctly referenced
        db_admin = config["mcpServers"].get("db_admin", {})
        hotel_agent = config["mcpServers"].get("hotel_agent", {})
        
        if "toolset_db_admin.yaml" in str(db_admin.get("args", [])):
            print("✅ DB admin toolset file correctly referenced")
        else:
            print("❌ DB admin toolset file incorrectly referenced")
            
        if "toolset_hotel_agent.yaml" in str(hotel_agent.get("args", [])):
            print("✅ Hotel agent toolset file correctly referenced")
        else:
            print("❌ Hotel agent toolset file incorrectly referenced")
            
    except Exception as e:
        print(f"❌ Error reading MCP configuration: {e}")


def test_toolset_files():
    """Test that the toolset files exist and are valid."""
    print("\n📁 Testing Toolset Files\n")
    
    toolset_files = [
        "config/toolset_db_admin.yaml",
        "config/toolset_hotel_agent.yaml"
    ]
    
    for toolset_file in toolset_files:
        if Path(toolset_file).exists():
            print(f"✅ {toolset_file} exists")
        else:
            print(f"❌ {toolset_file} not found")


def main():
    """Run all tests."""
    print("🧪 Testing MCP Time Server Integration\n")
    print("=" * 50)
    
    test_mcp_time_server_direct()
    test_timezone_resolution()
    test_cursor_mcp_config()
    test_toolset_files()
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("1. MCP time server should be configured in .cursor/mcp.json")
    print("2. Time server uses 'America/Denver' timezone (MDT)")
    print("3. Toolset files should reference the correct YAML files")
    print("4. Cursor IDE will automatically start the time server when needed")
    print("\n🎯 Next Steps:")
    print("- Restart Cursor IDE to load the new MCP configuration")
    print("- The time server will provide 'get_current_time' and 'convert_time' tools")
    print("- These tools will be available alongside your database tools")


if __name__ == "__main__":
    main() 