# Smart MCP Server Manager

This is an advanced system for managing Model Context Protocol (MCP) servers. It provides:

1. **Dynamic Port Scanning**: Automatically finds available ports for each server
2. **Dependency Management**: Installs required dependencies for each server
3. **Clean Shutdown**: Properly shuts down all servers when you're done
4. **Extensibility**: Easily add new MCP servers to the configuration

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

## Troubleshooting

If a server fails to start:

1. Check that all required environment variables are set in your `.env` file
2. Make sure you have a stable internet connection
3. Check that you have the latest version of Node.js and npm
4. Look for error messages in the console output

## Advanced Usage

You can customize the port ranges for each server in the configuration file. This is useful if you know that certain servers require specific ports.

You can also add custom environment variables for each server, which will be passed to the server process when it starts.
