// Simple script to test MCP servers
const fs = require('fs');
const { spawn } = require('child_process');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Function to test an MCP server
async function testMCPServer(serverName, command, args, env = {}) {
  console.log(`Testing ${serverName} MCP server...`);
  
  // Prepare environment variables
  const processEnv = { ...process.env };
  
  // Replace environment variable placeholders with actual values
  for (const [key, value] of Object.entries(env)) {
    if (value.startsWith('${') && value.endsWith('}')) {
      const envVarName = value.slice(2, -1);
      processEnv[key] = process.env[envVarName] || '';
    } else {
      processEnv[key] = value;
    }
  }
  
  // Start the MCP server process
  const serverProcess = spawn(command, args, { 
    env: processEnv,
    stdio: ['pipe', 'pipe', 'pipe']
  });
  
  // Handle process output
  serverProcess.stdout.on('data', (data) => {
    console.log(`${serverName} stdout: ${data}`);
  });
  
  serverProcess.stderr.on('data', (data) => {
    console.error(`${serverName} stderr: ${data}`);
  });
  
  // Wait for a short time to see if the server starts successfully
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  // Check if the process is still running
  if (serverProcess.killed) {
    console.error(`${serverName} server failed to start`);
    return false;
  }
  
  console.log(`${serverName} server started successfully`);
  
  // Kill the process after testing
  serverProcess.kill();
  return true;
}

// Main function to test all servers
async function testAllServers() {
  try {
    // Read the MCP configuration
    const configData = fs.readFileSync('mcp-config.json', 'utf8');
    const config = JSON.parse(configData);
    
    // Test each server
    for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
      const { command, args, env } = serverConfig;
      await testMCPServer(serverName, command, args, env);
      
      // Add a small delay between server tests
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    console.log('All MCP server tests completed');
  } catch (error) {
    console.error('Error testing MCP servers:', error);
  }
}

// Run the tests
testAllServers();
