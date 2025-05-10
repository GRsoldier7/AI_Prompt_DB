# Smart MCP Server Manager

This is an advanced system for managing Model Context Protocol (MCP) servers. It provides:

1. **Dynamic Port Scanning**: Automatically finds available ports for each server
2. **Dependency Management**: Installs required dependencies for each server
3. **Clean Shutdown**: Properly shuts down all servers when you're done
4. **Extensibility**: Easily add new MCP servers to the configuration
5. **Comprehensive Testing**: Includes test suites to verify server functionality

## Included MCP Servers

The Smart MCP Server Manager includes the following MCP servers:

1. **Context7**: Provides up-to-date documentation for libraries and frameworks
2. **Taskmaster**: AI-powered task management system
3. **Exa**: Web search capabilities for AI models
4. **Memory**: Persistent memory for AI models
5. **Knowledge**: Knowledge graph for AI models
6. **MCP-use**: Connects multiple MCP servers
7. **Heroku**: Heroku Platform MCP Server for managing Heroku apps, dynos, add-ons, and databases

## Quick Start

To start all MCP servers with automatic port allocation:

```
.\start_smart_mcp.bat
```

Or if you prefer PowerShell:

```
.\start_smart_mcp.ps1
```

## Adding New MCP Servers

To add a new MCP server to the configuration:

```
.\add_mcp_server.bat
```

Follow the prompts to configure your new server. The script will ask for:

- Server name
- Command to start the server
- Command arguments
- Port range
- Environment variables
- Dependencies to install

## Configuration

The system uses a configuration file (`mcp-servers-config.json`) to store information about all MCP servers. You can edit this file directly if you prefer.

Each server configuration includes:

- `command`: The command to run (e.g., `npx`, `node`, `python`)
- `args`: Command arguments as an array
- `env`: Environment variables
- `portRange`: The range of ports to try for this server
- `description`: A description of the server
- `dependencies`: Optional dependencies to install

### Heroku MCP Server Configuration

The Heroku MCP Server requires an API key to authenticate with the Heroku Platform. You can get this key by running:

```
heroku authorizations:create
```

Or by using an existing token:

```
heroku auth:token
```

Set the `HEROKU_API_KEY` environment variable with this token before running the Smart MCP Server Manager, or add it to your `.env` file:

```
HEROKU_API_KEY=your-token-here
```

The Heroku MCP Server provides tools for:

- Application Management: Deploy, scale, and manage Heroku apps
- Process & Dyno Management: Control dynos and processes
- Add-on Management: Provision and configure add-ons
- Database Management: Execute SQL queries and manage PostgreSQL databases
- Pipeline Management: Create and manage deployment pipelines

Example:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-package"],
      "env": {
        "API_KEY": "${MY_API_KEY}"
      },
      "portRange": {
        "start": 3601,
        "end": 3700
      },
      "description": "My custom MCP server",
      "dependencies": {
        "npm": ["my-package"],
        "pip": ["my-python-package"]
      }
    }
  }
}
```

## Global Settings

The configuration file also includes global settings:

- `defaultPortRange`: Default port range for new servers
- `scanAllPorts`: Whether to scan all ports before starting servers
- `autoInstallDependencies`: Whether to automatically install dependencies
- `startupDelay`: Delay between starting servers (in milliseconds)
- `maxStartupRetries`: Maximum number of retries if a server fails to start

## How It Works

1. The system scans all ports to find which ones are in use
2. It allocates available ports to each MCP server
3. It installs any required dependencies
4. It starts each server with the appropriate configuration
5. It provides a clean shutdown mechanism (Ctrl+C)

## Testing

The Smart MCP Server Manager includes comprehensive test suites to verify that everything is working correctly:

1. **Basic Tests**: Run `test_mcp_manager.bat` to check the basic functionality of the Smart MCP Server Manager.

2. **Comprehensive Tests**: Run `test_with_mock_server.bat` to test the Smart MCP Server Manager with a mock MCP server.

3. **Heroku MCP Server Tests**: Run `test_heroku_mcp.bat` to test the Heroku MCP Server integration.

Before running the Heroku MCP Server tests, make sure you have:
- Installed the Heroku CLI
- Set the `HEROKU_API_KEY` environment variable
- An active Heroku account

## Troubleshooting

If a server fails to start:

1. Check that all required environment variables are set in your `.env` file
2. Make sure you have a stable internet connection
3. Check that you have the latest version of Node.js and npm
4. Look for error messages in the console output
5. Run the appropriate test suite to diagnose the issue

## Advanced Usage

You can customize the port ranges for each server in the configuration file. This is useful if you know that certain servers require specific ports.

You can also add custom environment variables for each server, which will be passed to the server process when it starts.
