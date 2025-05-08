// Script to test individual MCP servers
const fs = require('fs');
const { spawn } = require('child_process');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config();

// Function to test a single MCP server
async function testServer(serverName) {
  try {
    // Read the MCP configuration
    const configPath = path.join(__dirname, 'mcp-config.json');
    const configData = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configData);
    
    // Check if the server exists in the config
    if (!config.mcpServers[serverName]) {
      console.error(`Server "${serverName}" not found in configuration`);
      return false;
    }
    
    const serverConfig = config.mcpServers[serverName];
    const { command, args, env = {} } = serverConfig;
    
    console.log(`Testing ${serverName} MCP server...`);
    
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
    
    return new Promise((resolve) => {
      // Start the MCP server process
      const serverProcess = spawn(command, args, { 
        env: processEnv,
        stdio: 'pipe'
      });
      
      let output = '';
      let errorOutput = '';
      let success = false;
      
      // Handle process output
      serverProcess.stdout.on('data', (data) => {
        const dataStr = data.toString();
        output += dataStr;
        console.log(`${serverName} output: ${dataStr.trim()}`);
        
        // Check for success indicators in the output
        if (dataStr.includes('Server started') || 
            dataStr.includes('listening') || 
            dataStr.includes('ready') ||
            dataStr.includes('MCP server started')) {
          success = true;
        }
      });
      
      serverProcess.stderr.on('data', (data) => {
        const dataStr = data.toString();
        errorOutput += dataStr;
        console.error(`${serverName} error: ${dataStr.trim()}`);
        
        // Some servers output to stderr even when successful
        if (dataStr.includes('Server started') || 
            dataStr.includes('listening') || 
            dataStr.includes('ready') ||
            dataStr.includes('MCP server started')) {
          success = true;
        }
      });
      
      // Set a timeout to check the server status
      setTimeout(() => {
        if (!serverProcess.killed) {
          console.log(`${serverName} server is running`);
          
          // If we haven't detected success but the server is still running, consider it a success
          if (!success && !errorOutput.includes('Error') && !errorOutput.includes('error')) {
            success = true;
          }
          
          // Kill the process
          serverProcess.kill();
          
          if (success) {
            console.log(`✅ ${serverName} server test PASSED`);
            resolve(true);
          } else {
            console.error(`❌ ${serverName} server test FAILED`);
            console.error(`Output: ${output}`);
            console.error(`Error: ${errorOutput}`);
            resolve(false);
          }
        } else {
          console.error(`❌ ${serverName} server test FAILED - process terminated unexpectedly`);
          resolve(false);
        }
      }, 10000); // Wait 10 seconds
      
      // Handle process exit
      serverProcess.on('error', (error) => {
        console.error(`Error starting ${serverName} server:`, error);
        resolve(false);
      });
      
      serverProcess.on('close', (code) => {
        if (code !== 0 && code !== null) {
          console.error(`${serverName} server exited with code ${code}`);
          resolve(false);
        }
      });
    });
  } catch (error) {
    console.error(`Error testing ${serverName} server:`, error);
    return false;
  }
}

// Main function
async function main() {
  // Get the server name from command line arguments
  const serverName = process.argv[2];
  
  if (!serverName) {
    console.error('Please provide a server name to test');
    console.log('Usage: node test_individual_server.js <server-name>');
    console.log('Available servers:');
    
    // Read the MCP configuration to list available servers
    const configPath = path.join(__dirname, 'mcp-config.json');
    const configData = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configData);
    
    Object.keys(config.mcpServers).forEach(name => {
      console.log(`- ${name}`);
    });
    
    process.exit(1);
  }
  
  // Test the specified server
  const success = await testServer(serverName);
  
  if (success) {
    console.log(`\n✅ ${serverName} server is working correctly`);
    process.exit(0);
  } else {
    console.error(`\n❌ ${serverName} server test failed`);
    process.exit(1);
  }
}

// Run the main function
main();
