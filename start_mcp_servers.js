// Script to start MCP servers
const fs = require('fs');
const { spawn } = require('child_process');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config();

// Function to start an MCP server
function startMCPServer(serverName, command, args, env = {}) {
  console.log(`Starting ${serverName} MCP server...`);
  
  // Prepare environment variables
  const processEnv = { ...process.env };
  
  // Replace environment variable placeholders with actual values
  for (const [key, value] of Object.entries(env)) {
    if (typeof value === 'string' && value.startsWith('${') && value.endsWith('}')) {
      const envVarName = value.slice(2, -1);
      processEnv[key] = process.env[envVarName] || '';
      if (!processEnv[key]) {
        console.warn(`Warning: Environment variable ${envVarName} is not set for ${serverName}`);
      }
    } else {
      processEnv[key] = value;
    }
  }
  
  // Start the MCP server process
  const serverProcess = spawn(command, args, { 
    env: processEnv,
    stdio: 'inherit'
  });
  
  // Handle process events
  serverProcess.on('error', (error) => {
    console.error(`Error starting ${serverName} server:`, error);
  });
  
  serverProcess.on('close', (code) => {
    console.log(`${serverName} server exited with code ${code}`);
  });
  
  return serverProcess;
}

// Main function to start all servers
function startAllServers() {
  try {
    // Read the MCP configuration
    const configPath = path.join(__dirname, 'mcp-config.json');
    const configData = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configData);
    
    const serverProcesses = {};
    
    // Start each server
    for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
      const { command, args, env } = serverConfig;
      serverProcesses[serverName] = startMCPServer(serverName, command, args, env);
    }
    
    console.log('All MCP servers started');
    
    // Handle process termination
    process.on('SIGINT', () => {
      console.log('Shutting down all MCP servers...');
      
      for (const [serverName, process] of Object.entries(serverProcesses)) {
        if (!process.killed) {
          console.log(`Stopping ${serverName} server...`);
          process.kill();
        }
      }
      
      console.log('All servers stopped');
      process.exit(0);
    });
    
  } catch (error) {
    console.error('Error starting MCP servers:', error);
  }
}

// Run the function
startAllServers();
