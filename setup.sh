#!/bin/bash

# Hotel Management Toolbox Setup Script
# This script sets up the complete hotel management system

set -e  # Exit on any error

echo "🏨 Hotel Management Toolbox Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed. Please install PostgreSQL first."
    echo "   On macOS: brew install postgresql"
    echo "   On Ubuntu: sudo apt-get install postgresql postgresql-contrib"
    echo "   On Windows: Download from https://www.postgresql.org/download/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    echo "🔧 Activating virtual environment (Windows)..."
    source venv/Scripts/activate
else
    echo "❌ Could not find virtual environment activation script."
    exit 1
fi

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    if [ -f "config/templates/.env.example" ]; then
        cp config/templates/.env.example .env
        echo "✅ .env file created from template"
        echo "⚠️  Please edit .env file with your actual credentials"
    else
        echo "❌ .env.example template not found"
        exit 1
    fi
else
    echo "✅ .env file already exists"
fi

# Setup database
echo "🗄️  Setting up database..."
if [ -f "scripts/setup/setup_database.sh" ]; then
    chmod +x scripts/setup/setup_database.sh
    ./scripts/setup/setup_database.sh
else
    echo "❌ Database setup script not found"
    exit 1
fi

# Setup MCP configuration (optional)
echo "🔗 Setting up MCP configuration (optional)..."
if [ -f "scripts/setup/setup_mcp.sh" ]; then
    chmod +x scripts/setup/setup_mcp.sh
    ./scripts/setup/setup_mcp.sh
    echo "✅ MCP configuration completed."
else
    echo "⚠️  MCP setup script not found. Skipping MCP configuration."
fi

# Make toolbox binary executable
if [ -f "bin/toolbox" ]; then
    chmod +x bin/toolbox
    echo "✅ Toolbox binary made executable"
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/tools/start_toolbox.sh
chmod +x scripts/setup/*.sh

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your actual credentials"
echo "2. Start the toolbox server: ./scripts/tools/start_toolbox.sh"
echo "3. Run the hotel agent: python main.py agent"
echo "4. Or run interactive mode: python main.py interactive"
echo ""
echo "For help: python main.py help"
echo ""
echo "Note: On Windows, activate your virtual environment with:"
echo "      venv\\Scripts\\activate" 