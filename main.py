#!/usr/bin/env python3

"""
Main entry point for the Hotel Management Toolbox.
Provides easy access to all system components.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config import Config
from src.agents.tests.test_agent_connectivity import run_test as run_agent_test
from src.agents.interactive_hotel_agent import interactive_hotel_agent


def print_banner():
    """Print the system banner."""
    print("🏨 Hotel Management Toolbox")
    print("=" * 40)
    print("A simple hotel management system powered by Google AI")
    print()


def print_usage():
    """Print usage information."""
    print("Usage:")
    print("  python main.py [command]")
    print()
    print("Commands:")
    print("  agent      - Run the agent connectivity test")
    print("  interactive - Run the interactive hotel agent")
    print("  config     - Show current configuration")
    print("  validate   - Validate configuration")
    print("  help       - Show this help message")
    print()
    print("Examples:")
    print("  python main.py agent")
    print("  python main.py interactive")
    print("  python main.py config")


def show_config():
    """Show current configuration."""
    print("📋 Current Configuration:")
    print("-" * 30)
    print(f"Database URL: {Config.get_database_url()}")
    print(f"Toolbox URL: {Config.get_toolbox_url()}")
    print(f"Google API Key: {'✅ Set' if Config.GOOGLE_API_KEY else '❌ Not set'}")
    print()


def validate_config():
    """Validate configuration."""
    print("🔍 Validating Configuration...")
    if Config.validate_config():
        print("✅ Configuration is valid!")
        return True
    else:
        print("❌ Configuration validation failed!")
        return False


async def main():
    """Main entry point."""
    print_banner()
    
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_usage()
    elif command == "config":
        show_config()
    elif command == "validate":
        validate_config()
    elif command == "agent":
        if validate_config():
            await run_agent_test()
        else:
            print("❌ Cannot run agent with invalid configuration")
    elif command == "interactive":
        if validate_config():
            await interactive_hotel_agent()
        else:
            print("❌ Cannot run interactive agent with invalid configuration")
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    asyncio.run(main()) 