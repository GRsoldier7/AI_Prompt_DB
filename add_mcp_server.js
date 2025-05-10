// Script to add a new MCP server to the configuration
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Function to prompt for input
function prompt(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

// Function to add a new MCP server
async function addMCPServer() {
  console.log('='.repeat(50));
  console.log('ADD NEW MCP SERVER TO CONFIGURATION');
  console.log('='.repeat(50));
  
  // Load the configuration file
  const configPath = path.join(__dirname, 'mcp-servers-config.json');
  let config;
  
  try {
    const configData = fs.readFileSync(configPath, 'utf8');
    config = JSON.parse(configData);
  } catch (error) {
    console.error(`Error loading configuration: ${error.message}`);
    console.log('Creating a new configuration file...');
    config = {
      mcpServers: {},
      settings: {
        defaultPortRange: { start: 3601, end: 4000 },
        scanAllPorts: true,
        autoInstallDependencies: true,
        startupDelay: 1000,
        maxStartupRetries: 3
      }
    };
  }
  
  // Get server information
  const serverName = await prompt('Enter server name (e.g., "my-server"): ');
  
  if (!serverName) {
    console.error('Server name is required');
    rl.close();
    return;
  }
  
  if (config.mcpServers[serverName]) {
    const overwrite = await prompt(`Server "${serverName}" already exists. Overwrite? (y/n): `);
    if (overwrite.toLowerCase() !== 'y') {
      console.log('Operation cancelled');
      rl.close();
      return;
    }
  }
  
  const command = await prompt('Enter command to start the server (e.g., "npx", "node", "python"): ');
  
  if (!command) {
    console.error('Command is required');
    rl.close();
    return;
  }
  
  const argsStr = await prompt('Enter command arguments (comma-separated, e.g., "-y,my-package"): ');
  const args = argsStr ? argsStr.split(',').map(arg => arg.trim()) : [];
  
  const description = await prompt('Enter server description: ');
  
  const portRangeStart = await prompt('Enter port range start (default: 3601): ');
  const portRangeEnd = await prompt('Enter port range end (default: 3700): ');
  
  const envVarsStr = await prompt('Enter environment variables (format: KEY=VALUE,KEY2=VALUE2): ');
  const env = {};
  
  if (envVarsStr) {
    const envPairs = envVarsStr.split(',');
    for (const pair of envPairs) {
      const [key, value] = pair.split('=').map(part => part.trim());
      if (key && value) {
        env[key] = value;
      }
    }
  }
  
  const installDeps = await prompt('Do you need to install dependencies? (y/n): ');
  let dependencies = null;
  
  if (installDeps.toLowerCase() === 'y') {
    const npmDepsStr = await prompt('Enter npm dependencies (comma-separated): ');
    const pipDepsStr = await prompt('Enter pip dependencies (comma-separated): ');
    
    dependencies = {};
    
    if (npmDepsStr) {
      dependencies.npm = npmDepsStr.split(',').map(dep => dep.trim());
    }
    
    if (pipDepsStr) {
      dependencies.pip = pipDepsStr.split(',').map(dep => dep.trim());
    }
  }
  
  // Create the server configuration
  config.mcpServers[serverName] = {
    command,
    args,
    env,
    portRange: {
      start: parseInt(portRangeStart) || 3601,
      end: parseInt(portRangeEnd) || 3700
    },
    description: description || `${serverName} MCP server`
  };
  
  if (dependencies) {
    config.mcpServers[serverName].dependencies = dependencies;
  }
  
  // Save the configuration
  try {
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
    console.log(`Server "${serverName}" added to configuration`);
    console.log('You can now start all servers with the smart MCP server manager');
  } catch (error) {
    console.error(`Error saving configuration: ${error.message}`);
  }
  
  rl.close();
}

// Run the function
addMCPServer();
