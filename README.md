# 🏨 Hotel Management Toolbox

A comprehensive hotel management system powered by Google AI and PostgreSQL, featuring intelligent agents for hotel search, booking, and management operations.

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd toolbox

# Copy environment template
cp config/templates/.env.example .env

# Edit .env with your credentials
nano .env
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Setup Database

```bash
# Run database setup
./scripts/setup/setup_database.sh
```

### 4. Start the System

```bash
# Start the toolbox server (required for CLI/scripts)
./scripts/tools/start_toolbox.sh

# In another terminal, run the hotel agent
python main.py agent
```

## 📁 Project Structure

```
toolbox/
├── src/
│   ├── agents/
│   │   ├── interactive_hotel_agent.py      # Interactive agent
│   │   └── tests/
│   │       └── test_agent_connectivity.py  # Agent connectivity test
│   ├── core/
│   └── utils/
│       ├── config.py
│       ├── time_utils.py                   # Time utility functions
│       └── __init__.py
├── config/
│   ├── toolset_db_admin.yaml               # Toolset for DB admin tools
│   ├── toolset_hotel_agent.yaml            # Toolset for hotel agent tools
│   └── templates/
│       ├── .env.example
│       └── .mcp.json.example
├── bin/
│   └── toolbox
├── scripts/
│   ├── setup/
│   │   ├── cursor/
│   │   │   ├── configure.sh
│   │   │   └── generate_mcp_json.py
│   │   ├── http/
│   │   └── setup_database.sh
│   └── tools/
│       └── start_toolbox.sh
├── examples/
│   ├── demo_interactive.py
│   ├── interactive_tool_test.py
│   ├── test_time_utils.py                  # Time utility tests
│   └── test_mcp_time_integration.py        # MCP time server tests
├── docs/
│   └── architecture.md
├── main.py
├── requirements.txt
└── .env
```

## 🔌 Cursor IDE Integration

This project is configured to integrate directly with the Cursor IDE through the Model Context Protocol (MCP), allowing you to use the defined tools right in the chat.

### MCP Servers

The project includes three MCP servers, each of which can be run in different modes depending on your workflow:

| Server        | Port  | Mode   | Managed By         |
|---------------|-------|--------|--------------------|
| db_admin      | 5051  | STDIO  | Cursor             |
| db_admin      | 5054  | HTTP   | User/Script        |
| hotel_agent   | 5052  | STDIO  | Cursor             |
| hotel_agent   | 5053  | HTTP   | User/Script        |
| time_server   | varies| HTTP   | User/Script/Cursor |

- **db_admin**: Database administration tools
  - STDIO mode (port 5051): Managed by Cursor for IDE integration.
  - HTTP mode (port 5054): For Python agents, Swagger UI, and direct HTTP access.
- **hotel_agent**: Hotel management tools
  - STDIO mode (port 5052): Managed by Cursor for IDE integration.
  - HTTP mode (port 5053): For Python agents, Swagger UI, and direct HTTP access.
- **time_server**: Time and timezone tools
  - HTTP mode only (default port, varies): Used by both Cursor and Python agents. Does not support STDIO/MCP protocol.

> **Note:** Only one mode (STDIO or HTTP) is supported per process. To support both, run two instances on different ports.
> **time_server** is HTTP-only and does not support STDIO/MCP protocol.

#### Viewing Running MCP Servers

You can use the `scripts/tools/list_mcp_servers.sh` script to view all running MCP servers, their ports, modes, and PIDs:

```bash
bash scripts/tools/list_mcp_servers.sh
```

This will print a table showing which servers are running, their connection mode, and their process IDs.

### Time Server Integration

The MCP time server provides timezone-aware functionality:

- **Current Time**: Get current time in any timezone
- **Time Conversion**: Convert times between different timezones
- **Timezone Support**: Uses IANA timezone identifiers (e.g., `America/Denver` for MDT)

**Available Tools:**
- `get_current_time`: Get current time in specified timezone
- `convert_time`: Convert time between timezones

**Configuration:**
- **Local Timezone**: Set to `America/Denver` (Mountain Daylight Time)
- **Server**: Automatically managed by Cursor IDE
- **Integration**: Seamlessly available alongside database tools

### Configuration

- **Configuration**: The integration is defined in the `.cursor/mcp.json` file.
- **Automatic Server Management**: You do **not** need to run `./scripts/tools/start_toolbox.sh` for the integration to work in Cursor. Cursor automatically starts and manages its own instance of the servers in the background.
- **Key Requirement**: The configuration in `.cursor/mcp.json` **must use absolute paths** for both the `toolbox` executable and the toolset YAML file. This is because Cursor does not run the server from the project's root directory.

To enable the tools, simply open the "Tools & Integrations" settings in Cursor and toggle the `postgres` tool on.

### Toolbox Server Startup Summary

| Environment   | Who Starts the Toolbox Server? | Why?                                      |
|--------------|-------------------------------|--------------------------------------------|
| Cursor IDE   | Cursor (automatically)        | Seamless UX, managed lifecycle             |
| CLI/Scripts  | User/Operator                 | Flexibility, explicit control, simplicity  |

## 🎯 Usage

### Main Entry Point

The `main.py` script provides easy access to all system components:

```bash
# Show help
python main.py help

# Run simple hotel agent demo
python main.py agent

# Run interactive hotel agent
python main.py interactive

# Show current configuration
python main.py config

# Validate configuration
python main.py validate
```

### Direct Script Usage

You can also run scripts directly:

```bash
# Interactive agent
python src/agents/interactive_hotel_agent.py

# Demo interactive features
python examples/demo_interactive.py

# Test individual tools
python examples/interactive_tool_test.py

# Agent connectivity test
python src/agents/tests/test_agent_connectivity.py

# Test time utilities
python examples/test_time_utils.py

# Test MCP time server integration
python examples/test_mcp_time_integration.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=toolbox_db
POSTGRES_USER=toolboxuser
POSTGRES_PASSWORD=your_password

# Toolbox Server Configuration
TOOLBOX_HOST=127.0.0.1
TOOLBOX_PORT=5001

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key
```

### Tool Configuration

The `config/toolset_db_admin.yaml` and `config/toolset_hotel_agent.yaml` files define the available toolsets:

- `toolset_db_admin.yaml`: Tools for database administration (list-tables, describe-table, execute-sql)
- `toolset_hotel_agent.yaml`: Tools for hotel management (list-hotels, bookings, etc.)

### Time Server Configuration

The MCP time server is configured with:
- **Local Timezone**: `America/Denver` (Mountain Daylight Time)
- **Server Type**: stdio-based MCP server
- **Integration**: Automatically available in Cursor IDE

## 🏗️ Architecture

The system follows a modular architecture:

```
User Interface (CLI/Python) → AI Agents → Toolbox Server → PostgreSQL Database
                                    ↓
                              MCP Time Server
```

### Components

1. **AI Agents** (`src/agents/`): Intelligent interfaces using Google AI
2. **Toolbox Server**: HTTP API server providing tool access
3. **MCP Time Server**: Timezone-aware time operations
4. **Database**: PostgreSQL with hotel and booking data
5. **Configuration**: Centralized config management (`src/utils/config.py`)

## 🧪 Testing

The primary method for testing is to use the interactive scripts provided in the `examples/` directory.

### Interactive Agent Demo
This script allows you to have a full, interactive conversation with the AI hotel agent, demonstrating the end-to-end functionality.

```bash
python examples/demo_interactive.py
```

### Time Server Testing
Test the MCP time server integration:

```bash
# Test time utilities
python examples/test_time_utils.py

# Test MCP time server integration
python examples/test_mcp_time_integration.py
```

## 🔄 Development

### Adding New Tools

1. Define the tool in the appropriate toolset YAML file (`config/toolset_db_admin.yaml` or `config/toolset_hotel_agent.yaml`)
2. Implement the tool logic in the toolbox server
3. Update the database schema if needed
4. Test with the interactive tool tester

### Adding New Agents

1. Create a new agent file in `src/agents/`
2. Import the `Config` utility from `src.utils.config`
3. Use the `ToolboxClient` to access tools
4. Add to `main.py` if needed

## 🚀 Deployment

### Production Setup

1. Set up PostgreSQL database
2. Configure environment variables
3. Start toolbox server as a service
4. Use reverse proxy (nginx) for production

### Docker Support

```bash
# Build and run with Docker (if Dockerfile provided)
docker build -t hotel-toolbox .
docker run -p 5001:5001 hotel-toolbox
```

## 📚 Documentation

- [Architecture Documentation](docs/architecture.md)
- [API Documentation](docs/api.md) (if available)
- [Development Guide](docs/development.md) (if available)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🤖 LLM Usage in the Architecture

- **App Layer (AI Agent):** Uses an LLM to interpret user queries, reason, select tools, and format responses.
- **Toolbox Server (MCP Server):** Does NOT use an LLM. It only executes tools (SQL, API calls, etc.) and returns structured data.

### Summary Table

| Component         | Uses LLM? | Purpose                                      |
|-------------------|-----------|----------------------------------------------|
| MCP/Toolbox Server| No        | Executes tools, runs SQL, returns data       |
| App Layer/Agent   | Yes       | Interprets user queries, reasons, formats    |
| Cursor IDE        | No*       | Sends tool requests, displays results        |

*Cursor can use an LLM for chat, but not for tool execution unless you wire it up that way.

See [docs/architecture.md](docs/architecture.md) for a full architecture diagram and more details.

---

**Note**: Make sure to set up your Google AI API key and PostgreSQL database before running the system. 