# AI Prompt Database with Smart MCP Server Manager

A comprehensive system for managing AI prompts and Model Context Protocol (MCP) servers, designed to provide high-quality prompts with easy access and usability, while efficiently managing multiple MCP servers with dynamic port allocation.

## Table of Contents

- [Overview](#overview)
- [AI Prompt Database](#ai-prompt-database)
  - [Features](#ai-prompt-database-features)
  - [Commands](#commands)
  - [Setup](#ai-prompt-database-setup)
  - [Requirements](#ai-prompt-database-requirements)
  - [Quality Standards](#quality-standards)
  - [Advanced Prompt Engineering](#advanced-prompt-engineering)
  - [Search Capabilities](#search-capabilities)
  - [Prompt Interaction](#prompt-interaction)
- [Smart MCP Server Manager](#smart-mcp-server-manager)
  - [Features](#smart-mcp-server-manager-features)
  - [Included MCP Servers](#included-mcp-servers)
  - [Architecture](#architecture)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Testing](#testing)
  - [Troubleshooting](#troubleshooting)
  - [Advanced Usage](#advanced-usage)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project combines a sophisticated AI Prompt Database with a Smart MCP Server Manager to create a powerful environment for AI-assisted development. The system is designed according to the principles outlined in the Vibe Coding Rulebook, ensuring high-quality code, comprehensive testing, and robust error handling.

## AI Prompt Database

The AI Prompt Database is a comprehensive tool for managing, categorizing, and optimizing AI prompts, designed to provide high-quality prompts with easy access and usability.

### AI Prompt Database Features

- **Prompt Management**: Store, retrieve, and organize prompts in a Google Sheet
- **Auto-categorization**: Automatically categorize prompts based on content
- **Effectiveness Analysis**: Rate prompts on their effectiveness
- **Prompt Improvement**: Generate improved versions of prompts
- **Batch Processing**: Process multiple prompts at once
- **Local Fallbacks**: Continue working even when API calls fail
- **Quality Standards**: Rigorous quality standards for clarity, precision, and contextual richness
- **Advanced Prompt Engineering**: Templates, parameterization, and constraints for refined outputs
- **Sophisticated Search**: Semantic search and faceted navigation for easy discovery
- **Streamlined Interaction**: One-click copy, formatted output, and direct integration with AI platforms

### Commands

- `python prompt_manager.py list` - List all prompts
- `python prompt_manager.py get --id <prompt_id>` - Get details of a specific prompt
- `python prompt_manager.py add --title <title> --text <text>` - Add a new prompt
- `python prompt_manager.py update --id <prompt_id> [options]` - Update an existing prompt
- `python prompt_manager.py analyze --id <prompt_id>` - Analyze a prompt's effectiveness
- `python prompt_manager.py improve --id <prompt_id>` - Generate an improved version of a prompt
- `python prompt_manager.py variations --id <prompt_id> --models <models>` - Generate variations of a prompt
- `python prompt_manager.py process-new` - Process all new prompts
- `python prompt_manager.py auto-fill --id <prompt_id>` - Auto-fill missing information for a prompt

### AI Prompt Database Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file:
   ```
   OPENROUTER_API_KEY=your_api_key
   OPENROUTER_MODEL=your_preferred_model
   GOOGLE_SHEETS_ID=your_google_sheet_id
   ```
4. Run the tool: `python prompt_manager.py list`

### AI Prompt Database Requirements

- Python 3.6+
- Google Sheets API credentials
- OpenRouter API key

### Quality Standards

The AI Prompt Database implements rigorous quality standards for all prompts:

1. **Clarity and Precision**: All prompts must be unambiguous and clearly state the desired output
2. **Contextual Richness**: Prompts include necessary context (target audience, tone, constraints)
3. **Iterative Refinement**: Prompts are continuously improved based on effectiveness ratings
4. **Effectiveness Validation**: Ratings are validated through user feedback and AI analysis

### Advanced Prompt Engineering

The database supports advanced prompt engineering techniques:

1. **Prompt Templates**: Structured templates for various tasks (creative writing, code generation, data analysis)
2. **Parameterization**: Defined placeholders that users can fill in via the UI
3. **Negative Prompts/Constraints**: Specific instructions on what to avoid or constraints to follow
4. **Analytics**: Track usage, ratings, and performance across different AI models

### Search Capabilities

Finding the right prompt is easy with sophisticated search capabilities:

1. **Semantic Search**: Understand user intent beyond keyword matching
2. **Faceted Navigation**: Filter by categories, subcategories, tools, ratings, and more
3. **Use-Case Driven Discovery**: Organize prompts by the problems they solve
4. **Personalization**: Save favorites, create collections, and receive recommendations

### Prompt Interaction

The database provides streamlined ways to use prompts:

1. **One-Click Copy**: Easily copy prompts to clipboard
2. **Formatted Output**: Preserve formatting for code or markup
3. **Direct Integration**: Send prompts directly to AI platforms
4. **Usage Guidance**: Comprehensive notes on how to use and modify prompts

## Smart MCP Server Manager

The Smart MCP Server Manager is an advanced system for managing Model Context Protocol (MCP) servers, providing dynamic port allocation, dependency management, and clean shutdown mechanisms.

### Smart MCP Server Manager Features

1. **Dynamic Port Scanning**: Automatically finds available ports for each server, preventing conflicts
2. **Dependency Management**: Installs required dependencies for each server automatically
3. **Clean Shutdown**: Properly shuts down all servers when you're done
4. **Extensibility**: Easily add new MCP servers to the configuration
5. **Comprehensive Testing**: Includes test suites to verify server functionality
6. **Error Resilience**: Implements retry mechanisms and robust error handling
7. **Resource Monitoring**: Tracks CPU and memory usage of running servers
8. **Structured Logging**: Provides detailed, parseable logs for debugging

### Included MCP Servers

The Smart MCP Server Manager includes the following MCP servers:

1. **Context7**: Provides up-to-date documentation for libraries and frameworks
2. **Taskmaster**: AI-powered task management system
3. **Exa**: Web search capabilities for AI models
4. **Memory**: Persistent memory for AI models
5. **Knowledge**: Knowledge graph for AI models
6. **MCP-use**: Connects multiple MCP servers
7. **Heroku**: Heroku Platform MCP Server for managing Heroku apps, dynos, add-ons, and databases

### Architecture

The Smart MCP Server Manager follows a modular architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                  Smart MCP Server Manager                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────┐   │
│  │ Port Scanner│   │ Config Loader│   │ Dependency Mgmt │   │
│  └─────────────┘   └─────────────┘   └─────────────────┘   │
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────┐   │
│  │ Server Mgmt │   │ Error Handler│   │ Logging System  │   │
│  └─────────────┘   └─────────────┘   └─────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
            │               │                │
            ▼               ▼                ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │ Context7 MCP│  │ Memory MCP  │  │ Heroku MCP  │
    └─────────────┘  └─────────────┘  └─────────────┘
            │               │                │
            └───────────────┼────────────────┘
                            │
                            ▼
                    ┌─────────────────┐
                    │  Your AI Models │
                    └─────────────────┘
```

### Installation

#### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Python 3.8+ (for certain MCP servers)
- Heroku CLI (for Heroku MCP server)

#### Setup

1. Clone the repository:
   ```
   git clone https://github.com/GRsoldier7/AI_Prompt_DB.git
   cd AI_Prompt_DB
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables by creating a `.env` file:
   ```
   ANTHROPIC_API_KEY=your_anthropic_key
   EXA_API_KEY=your_exa_key
   OPENROUTER_API_KEY=your_openrouter_key
   OPENROUTER_MODEL=your_preferred_model
   HEROKU_API_KEY=your_heroku_key
   ```

### Usage

#### Starting All MCP Servers

To start all MCP servers with automatic port allocation:

```
.\start_smart_mcp.bat
```

Or if you prefer PowerShell:

```
.\start_smart_mcp.ps1
```

#### Adding New MCP Servers

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

### Configuration

The system uses a configuration file (`mcp-servers-config.json`) to store information about all MCP servers. You can edit this file directly if you prefer.

#### Server Configuration Structure

Each server configuration includes:

- `command`: The command to run (e.g., `npx`, `node`, `python`)
- `args`: Command arguments as an array
- `env`: Environment variables
- `portRange`: The range of ports to try for this server
- `description`: A description of the server
- `dependencies`: Optional dependencies to install

#### Example Configuration

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

#### Heroku MCP Server Configuration

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

#### Global Settings

The configuration file also includes global settings:

- `defaultPortRange`: Default port range for new servers
- `scanAllPorts`: Whether to scan all ports before starting servers
- `autoInstallDependencies`: Whether to automatically install dependencies
- `startupDelay`: Delay between starting servers (in milliseconds)
- `maxStartupRetries`: Maximum number of retries if a server fails to start

### Testing

The Smart MCP Server Manager includes comprehensive test suites to verify that everything is working correctly:

1. **Basic Tests**: Run `test_mcp_manager.bat` to check the basic functionality of the Smart MCP Server Manager.

2. **Comprehensive Tests**: Run `test_with_mock_server.bat` to test the Smart MCP Server Manager with a mock MCP server.

3. **Heroku MCP Server Tests**: Run `test_heroku_mcp.bat` to test the Heroku MCP Server integration.

Before running the Heroku MCP Server tests, make sure you have:
- Installed the Heroku CLI
- Set the `HEROKU_API_KEY` environment variable
- An active Heroku account

### Troubleshooting

#### Common Issues and Solutions

1. **Server fails to start**:
   - Check that all required environment variables are set in your `.env` file
   - Make sure you have a stable internet connection
   - Check that you have the latest version of Node.js and npm
   - Look for error messages in the console output
   - Run the appropriate test suite to diagnose the issue

2. **Port conflicts**:
   - If you see "Address already in use" errors, try changing the port range in the configuration
   - Close other applications that might be using the same ports
   - Use `netstat -ano | findstr LISTENING` to identify which processes are using specific ports

3. **Dependency installation fails**:
   - Check your internet connection
   - Ensure you have the necessary permissions to install packages
   - Try installing the dependencies manually using `npm install` or `pip install`

4. **Environment variable issues**:
   - Make sure your `.env` file is in the correct location (root of the project)
   - Check for typos in environment variable names
   - Verify that the values are correct and properly formatted

5. **Heroku MCP Server specific issues**:
   - Ensure the Heroku CLI is installed and accessible in your PATH
   - Verify your Heroku API key is valid by running `heroku auth:whoami`
   - Check if your Heroku account has the necessary permissions

### Advanced Usage

#### Custom Port Ranges

You can customize the port ranges for each server in the configuration file. This is useful if you know that certain servers require specific ports.

#### Environment Variables

You can add custom environment variables for each server, which will be passed to the server process when it starts. Environment variables can reference other environment variables using the `${VARIABLE_NAME}` syntax.

#### Running Servers in Production

For production environments, consider:

1. Using a process manager like PM2:
   ```
   npm install -g pm2
   pm2 start smart_mcp_server.js
   ```

2. Setting up monitoring and alerts:
   ```
   pm2 monit
   ```

3. Configuring automatic restarts:
   ```
   pm2 startup
   pm2 save
   ```

### Security Considerations

1. **API Keys and Secrets**:
   - Store sensitive information in environment variables or a secure secrets manager
   - Never commit API keys or secrets to version control
   - Use the principle of least privilege when creating API keys

2. **Port Security**:
   - Avoid exposing MCP servers to the public internet unless necessary
   - Consider using a reverse proxy (like Nginx) for public-facing servers
   - Implement rate limiting and authentication for exposed endpoints

3. **Dependency Security**:
   - Regularly update dependencies to patch security vulnerabilities
   - Use `npm audit` to check for known vulnerabilities
   - Consider using tools like Snyk or Dependabot for automated security updates

### Performance Optimization

1. **Resource Management**:
   - Monitor CPU and memory usage of MCP servers
   - Adjust the number of concurrent servers based on available resources
   - Consider containerization (Docker) for better resource isolation

2. **Startup Optimization**:
   - Use the `startupDelay` setting to control the timing of server starts
   - Prioritize critical servers to start first
   - Consider lazy-loading servers that aren't immediately needed

3. **Logging Optimization**:
   - Use appropriate log levels to control verbosity
   - Implement log rotation to manage disk space
   - Consider using a centralized logging solution for easier analysis

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

Please make sure your code follows our coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
